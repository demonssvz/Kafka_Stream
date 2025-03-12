# 💰 Real-Time Currency Exchange Tracking using Apache Kafka





## 📌 **Project Overview**

This project implements a **real-time currency exchange tracking system** using **Apache Kafka** for stream processing. It allows financial analysts, traders, and businesses to track currency fluctuations **in real-time** and visualize exchange rate movements.

### **⚡ Key Features**

- **Real-time Data Streaming**: Fetches live currency exchange rates from [Fixer.io API](https://fixer.io/).
- **Apache Kafka Integration**: Ensures high-throughput and fault-tolerant data streaming.
- **Data Processing**: Uses Kafka Consumers for real-time validation and transformation.
- **Interactive Dashboard**: Built with **Streamlit** to visualize currency exchange rates.



---

## 🛠️ **Technology Stack**

| Technology                      | Purpose                                                   |
| ------------------------------- | --------------------------------------------------------- |
| **Apache Kafka**                | Real-time message broker for stream processing            |
| **Python**                      | Data fetching, transformation, and integration with Kafka |
| **Streamlit**                   | Interactive visualization dashboard                       |
| **Fixer.io API**                | Fetches live exchange rates                               |
| **Kafka Producers & Consumers** | Stream data to Kafka topics                               |
|                                 |                                                           |

---

## 🚀 **Project Setup & Installation**

### **1️⃣ Prerequisites**

- Install **Java 8+** (required for Kafka)
- Install \*\*Python \*\*
- Install **Apache Kafka** on your system

### **2️⃣ Kafka Installation on Windows**

1. **Download Kafka** from [Apache Kafka Downloads](https://kafka.apache.org/downloads).
2. Extract the ZIP and move it to `C:\kafka`.



### **3️⃣ Start Zookeeper & Kafka**

Run the following commands in **Command Prompt**:

```sh
cd C:\kafka
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

*Open a new terminal and start Kafka:*

```sh
cd C:\kafka
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

### **4️⃣ Create Kafka Topic**

```sh
.\bin\windows\kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic currency-exchange
```

### **5️⃣ Run the Kafka Producer (Data Ingestion)**

```sh
.\bin\windows\kafka-console-producer.bat --broker-list localhost:9092 --topic currency-exchange
```

*This will allow the producer to send exchange rate updates.*

### **6️⃣ Run the Kafka Consumer (Data Processing)**

```sh
.\bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic currency-exchange --from-beginning
```

*This will display real-time currency exchange data.*

---

## 📊 **System Architecture**

The system follows a **three-phase workflow**:
1️⃣ **Real-Time Data Ingestion**

- Fetches currency data from **Fixer.io API**.
- Uses **Kafka Producer** to send data to Kafka topics.

2️⃣ **Data Processing & Transformation**

- Kafka Consumers validate and transform the data.
- Stores processed data for real-time analytics.

3️⃣ **Data Visualization & Analysis**

- Uses **Streamlit** to display interactive currency exchange dashboards.
- Implements machine learning models for trend predictions.


---

## 📌 **How to Run the Visualization Dashboard**

1. Install the required dependencies:
   ```sh
   pip install streamlit kafka-python requests
   ```
2. Run the Streamlit dashboard:
   ```sh
   streamlit run dashboard.py
   ```
3. Open your browser and view the real-time exchange rate dashboard.

---

## 🎯 **Use Cases**

✔ **Forex Trading**: Helps traders analyze exchange rate fluctuations in real time.\
✔ **Stock Market Analytics**: Tracks real-time financial trends.\



### ⭐ **If you find this project useful, please ⭐ star this repository and contribute!**

