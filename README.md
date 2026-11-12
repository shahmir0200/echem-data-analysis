# Electrochemistry data analysis
During my internship I made catalysts that split water into hydrogen and oxygen (aka. electrolysis). I then tested their performance using a Potentiostat.
This python script takes the raw data from the Potentiostat and makes it into 2 graphs that compare the catalysts' performances.
The graphs are called LSV graphs (left) and Tafel plots (right). Both are used in electrochemistry to test catalyst performance.

## How graphs look in literature: 
<img width="620" height="254" alt="image" src="https://github.com/user-attachments/assets/7ed52b8f-42c9-4002-871b-e56003c8a00e" /> 

(source: Jones, C, et. al)

The performances of my catalysts are shown in mV/decade on the Tafel plot. The lower the value the better the catalyst performance. My results show that Co/CoP-HCN 1:5 has the best performance, which agrees with the literature.

Here is what my graphs look like after you run the code: 

<img width="1162" height="650" alt="image" src="https://github.com/user-attachments/assets/fd9cab38-53bf-40d9-ad88-6095ab838802" />

Here is what the raw data looked like from the Potentiostat: 

<img width="464" height="856" alt="image" src="https://github.com/user-attachments/assets/f1f6a96c-bbbd-4397-b676-fdc33e47e87a" />

I have uploaded a file of just the code, along with a file that explains the code in detail. I learned how to make this code using Gemini AI, by asking it to explain each line along the way. I then wrote a short description of what each line does to help me learn. 
