# DeData
![logo](https://github.com/user-attachments/assets/1dd84e66-c3f0-4b8b-8e6b-b1dcf208e56d)

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

![import_page](https://github.com/user-attachments/assets/982f855c-348c-48ef-b3f8-db933dff9e13)


The second page is the data visualization page, this page has two main functions.
The first one is printing your data set in a organized way and you can adjust it and save the new values. 
And making charts of your dataset.
![data_vis1](https://github.com/user-attachments/assets/e5343d18-ceba-46d5-bb95-307754c600b2)

![data_vis2](https://github.com/user-attachments/assets/00fca367-5f01-4796-9856-3d57a68ec0a4)


One thing I should explain it, is the data label , if I just load my file and try to enter the workspace or supervised or unsupervised pages, the program will refuse, because those 3 pages work with AI models, and you need to tale the AI models what you want to predict or estimate, so you must set a data label so the models understand that you will train them and then give them data without the data label column, and the model need to predict it.
![data_label1](https://github.com/user-attachments/assets/4f22523b-83ff-4ec3-9381-4ffc5f870919)

![data_label1](https://github.com/user-attachments/assets/ee6a32be-048a-4439-b81c-fe037ef44c55)

And we can change the data label in the Data Visualizetion by dubble click the wanted cloumn name.
![data_label3](https://github.com/user-attachments/assets/10574a11-660a-4d47-b686-88a66e77c3b5)
![data_label4](https://github.com/user-attachments/assets/b0268e2b-c235-4868-8241-0e4870aefba1)

Both of the supervised and unsupervised models pages have models taps, those taps when you click it,
![models1](https://github.com/user-attachments/assets/79a00df0-735f-4d2f-bdb1-6ae2597bc928)
![models2](https://github.com/user-attachments/assets/5a5ffb9e-516f-4865-a8a0-e6a5eefdf839)

a window will arise, this window is divided to two parts, the left part include the model description some images that demonstrate how the model work, and a parameters description, the right part include: firstly a checker that check if the model can work with the data label you have opted, or not, because some model work with class some with numbers and other advance things, and if the checker accept, you can use the model, if not you cannot and the checker will recommend an alternative model,
![models3](https://github.com/user-attachments/assets/a18ef95c-2f43-4bf7-8fbc-f1e9401ef32d)
![models4](https://github.com/user-attachments/assets/749de7f6-2c5d-4bc8-a16f-e554639346c0)

if you click use the model, the model will go to the work space page.
![work1](https://github.com/user-attachments/assets/5ae150e3-c78e-43ab-ba13-489442519205)
And each dataset has its own work space models.
![work2](https://github.com/user-attachments/assets/f66d6213-b425-4f3a-9e1d-d56122d42bab)

Than we have the work space page with same design of the supervised and unsupervised models pages, and a window will arise when click it, the right part of the window is very similar also, but with an adjustable parameters and model code, and both of the real and printed code get adjust when the user adjusts the parameters, so the user can compare between the parameters values.
![work_1](https://github.com/user-attachments/assets/9f8833b0-de5a-4bbc-be63-5779c83433e0)

The left part has also a checker, and down of it, we have a group of buttons, the first button is the train button, when you click it the model get trained.
![work2 (2)](https://github.com/user-attachments/assets/8e07add5-31cf-474a-8621-be88985c3314)
Down of it is the predict button when you click it a 3d window will arise, in it you put a new data and the model predict the label.
![work3](https://github.com/user-attachments/assets/fdb2bcb8-739e-4755-8502-e9f1e95b1684)
Down of it is the plot button with its own window also, in It you can plot some charts about the model performance. 
![work4](https://github.com/user-attachments/assets/4ae84eea-512f-4bdc-aa98-553085a09142)
Finally, the save model button, which save the model "trained" in 'sav' format in the saved_models folder, and when open the model next time, you will work in the same model, paramter, test score.

