# Reports3D
A web application which detects brain tumours and projects the model of the brain in AR. Reports3D employs the U-Net CNN architecture which detects and segments brain tumours based on MRI scans and renders the  volume of location and size of the tumour and brain. This volumetric rendering can e viewed in an Augmented Reality enviroment.

[**Model View in Website and Augmented Reality**](https://drive.google.com/file/d/15GeFuEADI5csEscKM4q-RJSdjKkSJ_TT/view?usp=sharing)

## Architecure

**The following image depicts the architecture of Reports3D:**
![Pipeline of our Model](https://github.com/Aditya-Salian/Reports3D/blob/master/Architecture.png)



## Results


**The segmentation results of our CNN are depicted in the image below:**
![Segmentation Results](https://github.com/Aditya-Salian/Reports3D/blob/master/SegmentationResults.png)


**The table below delineates the DSC scores for different regions of the tumour**
| | Mean Dice Similarity Coefficient | Median Dice Similarity Coefficient |
|-| -------------------------------- | ---------------------------------- |
| Full Tumour | 0.87 | 0.90 |
| Tumour Core | 0.76 | 0.84 |
| Enhancing Tumour | 0.71 | 0.80 |


**3-D Model Results**
| 3-D Model on web page | 3-D Model in Augmented Reality |
| ----------------------------- | -------------------------------------- |
| <img src ="https://github.com/Aditya-Salian/Reports3D/blob/master/ResultWeb.png" alt ="Web Page Model View" width = "512" height = "512" >|<img src ="https://github.com/Aditya-Salian/Reports3D/blob/master/ResultAR.png" alt = "AR Model View" width = "512" height = "512">|
