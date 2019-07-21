import cv2
import numpy as np


class Image_Stitching():
    def __init__(self) :
        self.ratio=0.85
        self.min_match=10
        # Initiate SIFT detector
        self.sift=cv2.xfeatures2d.SIFT_create()
        self.smoothing_window_size=100

    def registration(self,img1,img2):
        # find the keypoints and descriptors with SIFT
        kp1, des1 = self.sift.detectAndCompute(img1, None)
        kp2, des2 = self.sift.detectAndCompute(img2, None)

        # BFMatcher with default params
        matcher = cv2.BFMatcher()
        raw_matches = matcher.knnMatch(des1, des2, k=2)
        # Apply ratio test
        good_points = []
        good_matches=[]
        print(raw_matches)
        for m1, m2 in raw_matches:
            if m1.distance < self.ratio * m2.distance:
                good_points.append((m1.trainIdx, m1.queryIdx))
                good_matches.append([m1])
        # cv2.drawMatchesKnn expects list of lists as matches.
        img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good_matches, None, flags=2)
        cv2.imwrite('matching.jpg', img3)

        if len(good_points) > self.min_match:#If enough matches are found
            image1_kp = np.float32(
                [kp1[i].pt for (_, i) in good_points])
            image2_kp = np.float32(
                [kp2[i].pt for (i, _) in good_points])
            # findHomography returns a mask which specifies the inlier and outlier points.
			#RANSAC funtion to find out homography matrix
            H, status = cv2.findHomography(image2_kp, image1_kp, cv2.RANSAC,5.0)
        return H

    def create_mask(self,img1,img2,version):
		#use weighted matrix to create mask for blending images
        height_img1 = img1.shape[0]
        width_img1 = img1.shape[1]
        width_img2 = img2.shape[1]
        height_panorama = height_img1
        width_panorama = width_img1 + width_img2
        offset = int(self.smoothing_window_size / 2)
        barrier = img1.shape[1] - int(self.smoothing_window_size / 2)
        mask = np.zeros((height_panorama, width_panorama))
        if version == 'left_image':
            mask[:, barrier - offset:barrier + offset ] = np.tile(np.linspace(1, 0, 2 * offset ).T, (height_panorama, 1))
            mask[:, :barrier - offset] = 1
        else:
            mask[:, barrier - offset:barrier + offset ] = np.tile(np.linspace(0, 1, 2 * offset ).T, (height_panorama, 1))
            mask[:, barrier + offset:] = 1
        return cv2.merge([mask, mask, mask])

    def blending(self,img1,img2):
		#stitching two images funtion
        H = self.registration(img1,img2)
        height_img1 = img1.shape[0]
        width_img1 = img1.shape[1]
        width_img2 = img2.shape[1]
        height_panorama = height_img1
        width_panorama = width_img1 +width_img2

        panorama1 = np.zeros((height_panorama, width_panorama, 3))
        mask1 = self.create_mask(img1,img2,version='left_image')
        panorama1[0:img1.shape[0], 0:img1.shape[1], :] = img1
        panorama1 *= mask1
        mask2 = self.create_mask(img1,img2,version='right_image')
        panorama2 = cv2.warpPerspective(img2, H, (width_panorama, height_panorama))*mask2
        result=panorama1+panorama2
        cv2.imwrite('pano1.jpg', panorama1)
        cv2.imwrite('pano2.jpg', panorama2)
        cv2.imwrite('result.jpg', result)
        rows, cols = np.where(result[:, :, 0] != 0)
        min_row, max_row = min(rows), max(rows) + 1
        min_col, max_col = min(cols), max(cols) + 1
        final_result = result[min_row:max_row, min_col:max_col, :]
        return final_result
def runPano(linkList):
    img1 = cv2.imread(linkList[0])
    temp = img1
    del linkList[0]
    while linkList:

        img2 = cv2.imread(linkList[0])
        rs1 = Image_Stitching().blending(temp, img2)
        rs2 = Image_Stitching().blending(img2, temp)
        if (rs1.shape[1] > rs2.shape[1]):
            temp = rs1
        elif (rs1.shape[1] < rs2.shape[1]):
            temp = rs2
        else:
            linkList.append(linkList[0])
        cv2.imwrite('panorama.jpg', temp)
        temp = cv2.imread('panorama.jpg')
        del linkList[0]
def main():


    s1 = "e1.jpg"
    s2 = "e2.jpg"
    s3 = "e3.jpg"
    s4 = "e4.jpg"

    linkList =[s1,s2,s3,s4]
    img1 = cv2.imread(linkList[0])
    temp = img1
    del linkList[0]
    while linkList:

        img2 = cv2.imread(linkList[0])
        rs1 = Image_Stitching().blending(temp, img2)
        rs2 = Image_Stitching().blending(img2, temp)
        if (rs1.shape[1] > rs2.shape[1]):
            temp = rs1
        elif (rs1.shape[1] < rs2.shape[1]):
            temp = rs2
        else:
            linkList.append(linkList[0])
        cv2.imwrite('panorama.jpg', temp)
        temp = cv2.imread('panorama.jpg')
        del linkList[0]
    # return final
if __name__ == '__main__':
    try:
        main()
    except IndexError:
        print("Please input two source images: ")



