# dashboard-ecommerce


Dashboard ini dibuat menggunakan **Streamlit** untuk menampilkan hasil analisis data secara interaktif, termasuk analisis penjualan dan segmentasi pelanggan menggunakan metode **RFM (Recency, Frequency, Monetary)**.

---

## 📊 Fitur Dashboard

* 📈 Visualisasi tren penjualan bulanan
* 🏆 Top 10 kategori produk
* 👥 Segmentasi pelanggan menggunakan RFM Analysis
* 📋 Tabel data RFM
* 🧠 Insight dan rekomendasi bisnis

---

## ⚙️ Setup Environment

### 🔹 Menggunakan Anaconda

```bash
conda create --name dashboard-env python=3.9
conda activate dashboard-env
pip install -r requirements.txt
```

---

### 🔹 Menggunakan Virtual Environment (Terminal)

```bash
mkdir proyek_analisis_data
cd proyek_analisis_data

python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

---

## 📦 Install Dependencies

Pastikan file `requirements.txt` berisi:

```txt
streamlit
pandas
plotly
```

Lalu install dengan:

```bash
pip install -r requirements.txt
```

---

## ▶️ Menjalankan Dashboard

Jalankan perintah berikut di terminal:

```bash
streamlit run app.py
```

Setelah itu, buka browser dan akses:

```
http://localhost:8501
```

---

## 📁 Struktur Proyek

```
project/
│
├── dashboard.py
├── customers_dataset.csv
├── orders_dataset.csv
├── order_items_dataset.csv
├── products_dataset.csv
├── product_category_name_translation.csv
├── requirements.txt
└── README.md
```

---

## 🧠 Insight yang Dihasilkan

Dashboard ini memberikan insight seperti:

* Total revenue dan performa penjualan
* Kategori produk dengan penjualan tertinggi
* Segmentasi pelanggan berdasarkan RFM:

  * Champions
  * Loyal Customers
  * Potential Loyalist
  * At Risk
  * Lost
* Rekomendasi strategi bisnis berbasis data

---

## 🚀 Deployment (Opsional)

Dashboard dapat dideploy menggunakan:

* Streamlit Community Cloud
* GitHub sebagai repository utama

---

## 👨‍💻 Author

Proyek ini dibuat untuk memenuhi tugas **Proyek Analisis Data**.

---
