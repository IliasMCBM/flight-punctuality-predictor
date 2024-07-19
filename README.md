# Flight Punctuality Predictor (FPP)

## Introduction
Flight delays present a critical issue for airlines, impacting operational efficiency and causing substantial financial repercussions. The primary goal of this project is to develop a predictive model to forecast flight punctuality, thereby enabling airlines to mitigate delays and enhance overall efficiency.

## Storytelling
Flight delays cost airlines billions of dollars annually. For instance, in the United States alone, flight delays and cancellations amounted to approximately $28 billion in direct costs in 2019, according to the Federal Aviation Administration (FAA). Operational disruptions due to delays lead to cascading effects such as missed connections and scheduling conflicts. On average, over 20% of flights worldwide are delayed, causing widespread inconvenience for passengers.

Consider the case of Singapore Changi Airport, renowned for its operational efficiency and world-class service. Changi Airport meticulously times its maintenance and cleaning operations to ensure smooth transitions and minimal downtime between flights. However, even minor delays can have significant repercussions. For instance, if a single flight is delayed, it can cause a domino effect, leading to gate hold-ups, rescheduling of ground services, and increased congestion on the runways. This can disrupt the tightly coordinated operations, leading to inefficiencies and increased operational costs. Moreover, the high standards of service expected at Changi mean that delays can severely impact passenger satisfaction and the airport’s reputation for punctuality and reliability.

Customer satisfaction also takes a hit. According to a study by J.D. Power, satisfaction levels among passengers decrease by 50 points when flights are delayed by just 15 minutes. Dissatisfied passengers may choose alternative airlines for future travel, affecting revenue and market share. Moreover, flight delays tarnish the reputation of airlines, eroding trust and loyalty among passengers. High-profile delays can generate negative publicity and social media backlash, further damaging the brand image of airlines and influencing consumer perception.

To tackle this problem, I decided to create the Flight Punctuality Predictor. This innovative solution leverages advanced machine learning techniques to analyze historical flight data and various influencing factors to provide airlines with actionable insights. Unlike existing solutions that focus solely on historical data analysis or real-time flight tracking, our predictor integrates both, offering real-time predictions that empower airlines to anticipate potential delays and take proactive measures.

## Technical Part
The Flight Punctuality Predictor uses a combination of Docker, Python, Pandas, scikit-learn, XGBoost, FastAPI, Uvicorn, and Nginx to deliver a robust and efficient solution.

- **Docker** ensures consistency and portability across different environments, making it easier to deploy and manage the application.
- **Python** serves as the primary programming language, utilized for data manipulation and machine learning tasks.
- **Pandas** is employed for data manipulation and preprocessing, cleaning and preparing the extensive historical flight data for analysis.
- **scikit-learn** is used to develop and train the predictive model for flight delays, while **XGBoost** enhances model accuracy and performance.
- **FastAPI** provides a robust framework for building the backend web API, and **Uvicorn** runs the FastAPI application, ensuring high performance.
- **Nginx** manages incoming traffic and ensures smooth operation of the deployed application.

## How to Execute and Use It
For development and testing, I am using PyCharm as my Integrated Development Environment (IDE). PyCharm facilitates coding, debugging, and managing the project efficiently. 

To run the Flight Punctuality Predictor, you need Docker installed on your system and virtualization enabled in the BIOS. Follow these steps to get the application up and running:

### Clone the Repository:
```bash
git clone https://github.com/IliasMCBM/flight-punctuality-predictor.git
