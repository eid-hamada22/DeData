# DeData
![logo](https://github.com/user-attachments/assets/3fdb96ec-f254-4d98-a9cf-364c004ef984)

PyQt5 Hands-on Machine-Learning Educational App.

Made with Passion.
War Bloodstained project that was planned to be my main [RISE](https://www.risefortheworld.org/) project, however, due to Internet and electrcity cutoff, I didn't manage to upload it.

## used Tools and techniques :
- Python.
- PyQt5 framework.
- Sqlite database.
- Sklearn.
- Numpy.
- Pandas.
- Pickle.
- Matplotlib.


## Development period: +4 months.

Essentially, my program work with data sets, you give it a data set and it make use of it in another sections, the first page is the page that take the dataset from the user.
And there are 3 ways, first by load it from the user device as file or by load the file from the web using its direct URL, or use the demo datasets which come built in with the program. 

![import_page](https://github.com/user-attachments/assets/c28e901c-9b7b-4346-b271-63d28f186867)


The second page is the data visualization page, this page has two main functions.
The first one is printing your data set in a organized way and you can adjust it and save the new values. 
And making charts of your dataset.
![data_vis1](https://github.com/user-attachments/assets/bc1dbe3c-38b8-4c37-bfce-cb373e9b0bbf)

![data_vis2](https://github.com/user-attachments/assets/d0f69370-98d4-4d62-8e9d-696b339920a2)


One thing I should explain it, is the data label , if I just load my file and try to enter the workspace or supervised or unsupervised pages, the program will refuse, because those 3 pages work with AI models, and you need to tale the AI models what you want to predict or estimate, so you must set a data label so the models understand that you will train them and then give them data without the data label column, and the model need to predict it.
![data_label1](https://github.com/user-attachments/assets/0867893f-8b61-4fcd-b8d1-76e8377f71f6)

![data_label2](https://github.com/user-attachments/assets/7a54575d-30d9-4ef2-ad90-ff09fe5c019d)

And we can change the data label in the Data Visualizetion by dubble click the wanted cloumn name.
![data_label3](https://github.com/user-attachments/assets/b8bdcc11-e97e-4c44-8c23-3206741fee2b)
![data_label4](https://github.com/user-attachments/assets/b23c94c2-f234-4df5-bdc4-0afcb6bc9571)

Both of the supervised and unsupervised models pages have models taps, those taps when you click it,
![models1](https://github.com/user-attachments/assets/8c827653-7085-4e41-a7be-fbb20defee21)
![models2](https://github.com/user-attachments/assets/2e72e02a-0c74-40fa-940e-a199b1dfaa6e)

a window will arise, this window is divided to two parts, the left part include the model description some images that demonstrate how the model work, and a parameters description, the right part include: firstly a checker that check if the model can work with the data label you have opted, or not, because some model work with class some with numbers and other advance things, and if the checker accept, you can use the model, if not you cannot and the checker will recommend an alternative model,
![models3](https://github.com/user-attachments/assets/e4375867-0239-421b-8dc8-a6af0a898ae2)
![models4](https://github.com/user-attachments/assets/f7b356f6-e8b2-4b5d-a2b8-64422059000d)

if you click use the model, the model will go to the work space page.
![work1](https://github.com/user-attachments/assets/ed0b87a5-31c4-4ac6-9c4d-55ad2f554c32)

And each dataset has its own work space models.
![work2](https://github.com/user-attachments/assets/3c7e170a-2164-42ff-853e-1aabf90e343d)

Than we have the work space page with same design of the supervised and unsupervised models pages, and a window will arise when click it, the right part of the window is very similar also, but with an adjustable parameters and model code, and both of the real and printed code get adjust when the user adjusts the parameters, so the user can compare between the parameters values.
![work_1](https://github.com/user-attachments/assets/2f2f27f9-e800-4fca-8fd8-f3f2797e7e4f)

The left part has also a checker, and down of it, we have a group of buttons, the first button is the train button, when you click it the model get trained.
![work2 (2)](https://github.com/user-attachments/assets/5d403142-aa2d-404b-bf70-8afd38d6de89)

Down of it is the predict button when you click it a 3d window will arise, in it you put a new data and the model predict the label.
![work3](https://github.com/user-attachments/assets/2505c079-add7-45b0-a1ba-c5bebefcf742)


Down of it is the plot button with its own window also, in It you can plot some charts about the model performance. 
![work4](https://github.com/user-attachments/assets/3b569683-d43f-41c8-95a1-46b034376c63)

Finally, the save model button, which save the model "trained" in 'sav' format in the saved_models folder, and when open the model next time, you will work in the same model, paramter, test score.
![work5](https://github.com/user-attachments/assets/5546f951-8085-4aa2-a4d6-c82a2e23df73)

