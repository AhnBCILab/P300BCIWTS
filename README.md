**World Tour System(WTS)**
==========================
## ↓↓ Click on the picture below to see the demonstration video of WTS!! ↓↓ ##
[![Watch the video](https://img.youtube.com/vi/kmGgAUAVbds/maxresdefault.jpg)](https://youtu.be/kmGgAUAVbds)  

**System Overview**
-------------------
### World Tour System (WTS) is a world tour BCI application using P300 brain waves.

### The system is divided into two types depending on the existence of a training session:
* **Within session:** It extracts significant features from user data through training sessions and then trains them to generate LDA classifiers and use it to predict target buttons.
* **Zero session:** It has no training session, and it works by using the CNN model in an online session that predict the target button.

### The following figure is the system diagram of WTS.
![WTS_SystemDiagram](./Image/WTS_SystemDiagram.png)
### ※ Update ※
OpenViBE's Python Scripting box does not yet support Python 3. In a situation where the CNN model needs to be introduced in WTS, the system is divided into three modules to operate in order to use tensorflow in Python 3. The method of operating the new method of WTS was described in detail in step-by-step in the Documentation.

* If you want to use the old WTS, you can implement the function in SourceCode/ProcessingWorld.py and call the function in the second for statement in the def process part of Within/SourceCode/WorldOnline.py. Details are described in Documentation.


### WTS system proceeds as follows.
![WTS_Flowchart](./Image/WTS_Flowchart.jpg)

### See the WTS_Documentation.pdf file for details.
### Or contact BCI LAB: https://bcilab.handong.edu/contact

### Video sources
#### Europe
paris
https://www.youtube.com/watch?v=OFK0vkGsaTU

London
https://www.youtube.com/watch?v=HHll-xZpdjI&list=PLFbrGwG_kJl2mnuWRKg3I5vpvxJFi5Fil&index=5

Rome
https://www.youtube.com/watch?v=Y7W2FOJXjZo&index=8&list=PLFbrGwG_kJl2mnuWRKg3I5vpvxJFi5Fil

Barcelona
https://www.youtube.com/watch?v=hw5oyLG9EyI&list=PLFbrGwG_kJl2mnuWRKg3I5vpvxJFi5Fil

Iceland
https://www.youtube.com/watch?v=jz3QsIAm2D4&index=2&list=PLFbrGwG_kJl2mnuWRKg3I5vpvxJFi5Fil

Firenze
https://www.youtube.com/watch?v=ycz8PCltH1c


#### Asia
Seoul
https://www.youtube.com/watch?v=mxbTKd7uUjA

Dubai
https://www.youtube.com/watch?v=pIMV6_cKamw&list=PLFbrGwG_kJl2mnuWRKg3I5vpvxJFi5Fil&index=9

HongKong
https://www.youtube.com/watch?v=MhFC9Ke-IbA&index=14&list=PLFbrGwG_kJl2mnuWRKg3I5vpvxJFi5Fil

India
https://www.youtube.com/watch?v=_8OqpOAS4j4

Tokyo
https://www.youtube.com/watch?v=kzMeZfF2Xgs

Shanghai
https://www.youtube.com/watch?v=qafzoWnmDSg


#### North America
Vancouver
https://www.youtube.com/watch?v=4rtcCHfHnpg&list=PLFbrGwG_kJl2mnuWRKg3I5vpvxJFi5Fil&index=10

NewYork
https://www.youtube.com/watch?v=wTdnTjbQ52A&index=15&list=PLFbrGwG_kJl2mnuWRKg3I5vpvxJFi5Fil

LasVegas
https://www.youtube.com/watch?v=cKD57Jr5wpQ

LosAngeles
https://www.youtube.com/watch?v=ojplJASZ02w

Chicago
https://www.youtube.com/watch?v=bR_IzJ73DFE

Alaska
https://www.youtube.com/watch?v=BKkqmhv1bdA


#### Oceania
Sydney
https://www.youtube.com/watch?v=IWMlmf2-RFw

Melbourne
https://www.youtube.com/watch?v=KnTicgTnF4M

Fiji
https://www.youtube.com/watch?v=JRaakIL-N_s

NewZealand
https://www.youtube.com/watch?v=fHCemviY06Y

Papua New Guinea
https://www.youtube.com/watch?v=hEbkzR7-3Gk

Vanuatu
https://www.youtube.com/watch?v=gOwSz3rCV8Q


#### South America
Barbados
https://www.youtube.com/watch?v=y2CN5VrnR9g&list=PLFbrGwG_kJl2mnuWRKg3I5vpvxJFi5Fil&index=3

Easter Island
https://www.youtube.com/watch?v=tZpGCFEw8Jg&index=7&list=PLFbrGwG_kJl2mnuWRKg3I5vpvxJFi5Fil

Patagonia
https://www.youtube.com/watch?v=4UW57_fN4dY

Cusco (37:02~47:02)
https://www.youtube.com/watch?v=N50PhJ4Pr1Q

Rio de Janeiro
https://www.youtube.com/watch?v=9lnxGcax1ok

BuenosAires
https://www.youtube.com/watch?v=nj3FnGV-0L4


#### Africa
Egypt
https://www.youtube.com/watch?v=4uXLHc67vvk

CapeTown
https://www.youtube.com/watch?v=Rfw9YZzf2ak

Johannesburg
https://www.youtube.com/watch?v=2qTsWpB939Y

Nairobi (0:14 ~ 0:24)
https://www.youtube.com/watch?v=4sl3hko3tJU

Pretoria East (0:05 ~ 0:15)
https://www.youtube.com/watch?v=tNGpklQ_97Y

Ethiopia
https://www.youtube.com/watch?v=2WAwquxIi4c

