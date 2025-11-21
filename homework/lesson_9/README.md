# Task: Predicting Apartment Prices in Prague

## Overview
The goal of this assignment is to **predict the listing price of apartments in Prague** using the provided dataset.  
Models will be evaluated using **Mean Absolute Percentage Error (MAPE)**.

Both training and test datasets come from the same distribution.

---

## Datasets
You are given:

- **Training dataset (`train.csv`)**  
  Contains all columns, including `price`.

- **Test dataset (`test.csv`)**  
  Contains the same columns *except* `price`.  
  Your task is to predict this missing value.

---

## Evaluation Metric

### Mean Absolute Percentage Error (MAPE)
Formula and explanation:  
<https://en.wikipedia.org/wiki/Mean_absolute_percentage_error>

Lower MAPE = better performance.

---

## Submission Format
Submit a **CSV file** with exactly two columns:

| id | price           |
|----|-----------------|
| apartment_id | predicted_price |

Any additional columns will be ignored.

A submission form will be provided later.

---

## Allowed Methods
You may use **any machine learning model or pipeline**, including:

- Linear and non-linear regression models
- Tree-based methods (Random Forest, Gradient Boosting, etc.)
- Neural networks
- Custom feature engineering and preprocessing

---

## Column Description

### Identifiers
- `id` – Unique identifier.
- `address` – Full street address.

### Layout
- `layout` – Apartment layout (e.g., `1+kk`, `2+1`, `3+kk`).
- `price` – Price in CZK (**present only in the training set**).

### Location
- `gps_lat`, `gps_lon` – GPS coordinates.

### Apartment Details
- `area` – Floor area (m²).
- `floor` – Floor number.
- `total_floors` – Total number of floors in the building.
- `construction` – Construction type (e.g., `Brick`, `Panel`).
- `condition` – Apartment condition (e.g., `New`, `Renovated`).
- `ownership` – Ownership type (e.g., `Personal`, `Cooperative`).

### Additional Features
- `cellar_area` – Cellar size in m².
- `balcony_area` – Balcony size in m².
- `garden_area` – Garden size in m².
- `elevator` – Elevator availability (`Yes`, `No`, or empty).
- `parking` – Number of parking spots.

### Points of Interest — Counts
- `poi_doctors_count` – Number of doctors/clinics nearby.
- `poi_leisure_time_count` – Number of leisure locations.
- `poi_school_kindergarten_count` – Number of schools/kindergartens.
- `poi_transport_count` – Number of public transport stops.
- `poi_grocery_count` – Number of grocery stores.
- `poi_restaurant_count` – Number of restaurants.

### Points of Interest — Nearest Distances
(All distances are in meters.)

- `poi_doctors_nearest` – Distance to the nearest doctor.
- `poi_leisure_time_nearest` – Distance to the nearest leisure location.
- `poi_school_kindergarten_nearest` – Distance to the nearest school/kindergarten.
- `poi_transport_nearest` – Distance to the nearest public transport stop.
- `poi_grocery_nearest` – Distance to the nearest grocery store.
- `poi_restaurant_nearest` – Distance to the nearest restaurant.

### Advertisement Information
- `text` – Listing description text.
- `first_seen` – Date when the listing was first recorded.
- `last_seen` – Date when the listing was last recorded.
