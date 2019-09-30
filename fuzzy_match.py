from PIL import Image


def fuzzy_similarity(img1, img2):
    l_img1 = img1.convert("L")
    l_img2 = img2.convert("L")
    width = l_img1.size[0]
    height = l_img1.size[1]
    data_1 = list(l_img1.getdata())
    data_2 = list(l_img2.getdata())
    MSE = 0
    for i in range(len(data_1)):
        MSE += (data_1[i] - data_2[i]) * (data_1[i] - data_2[i])
    return MSE / width / height


def fuzzy_images_match(img, list_of_img):
    MSEs = []
    for candidate in list_of_img:
        MSEs.append(fuzzy_similarity(img, candidate))
    # print(MSEs)
    if min(MSEs) < 1000:
        return MSEs.index(min(MSEs))
    else:
        return 0

# MSE = fuzzy_similarity(Image.open("digit6.png"), Image.open("digit9.png"))
# print(MSE)