library(tidyverse)

train <- read_csv("appartments_train.csv")
test  <- read_csv("appartments_test.csv")

# Look at data

glimpse(train)
summary(train$price)

# Missing values

missing_train <- train %>% 
  summarise(across(everything(), ~ sum(is.na(.)))) %>% 
  pivot_longer(everything(),
               names_to = "column",
               values_to = "na_count") %>% 
  arrange(desc(na_count))


missing_test <- test %>% 
  summarise(across(everything(), ~ sum(is.na(.)))) %>% 
  pivot_longer(everything(),
               names_to = "column",
               values_to = "na_count") %>% 
  arrange(desc(na_count))

# Histogram price

train %>%
  ggplot(aes(price)) +
  geom_histogram(bins = 40, fill = "steelblue") +
  theme_minimal() +
  labs(title = "Histogram ceny bytu", x = "Cena", y = "Počet")

# Boxplot cien vs elevator

train %>%
  mutate(elevator_group = ifelse(is.na(elevator), "Unknown", elevator)) %>%
  ggplot(aes(x = elevator_group, y = price)) +
  geom_boxplot(fill = "steelblue", alpha = 0.7) +
  theme_minimal() +
  labs(
    title = "Cena bytu podľa elevator (Yes / No / Unknown)",
    x = "Elevator",
    y = "Cena"
  )

# pomocná funkcia na imputáciu jedného datasetu
clean_data <- function(df) {
  
  # 1. NA → 0 (logické absencie)
  df <- df %>%
    mutate(
      garden_area  = replace_na(garden_area, 0),
      balcony_area = replace_na(balcony_area, 0),
      cellar_area  = replace_na(cellar_area, 0),
      parking      = replace_na(parking, 0)
    )
  
  # 2. elevator → Unknown
  df <- df %>%
    mutate(
      elevator = ifelse(is.na(elevator), "Unknown", elevator)
    )
  
  # 3. total_floors → medián podľa construction
  df <- df %>%
    group_by(construction) %>%
    mutate(
      total_floors = ifelse(
        is.na(total_floors),
        median(total_floors, na.rm = TRUE),
        total_floors
      )
    ) %>%
    ungroup()
  
  # 4. POI nearest → medián naprieč dátami
  poi_nearest <- c(
    "poi_doctors_nearest",
    "poi_leisure_time_nearest",
    "poi_school_kindergarten_nearest",
    "poi_transport_nearest",
    "poi_grocery_nearest",
    "poi_restaurant_nearest"
  )
  
  df <- df %>%
    mutate(across(all_of(poi_nearest),
                  ~ replace_na(.x, median(.x, na.rm = TRUE))))
  
  return(df)
}

# aplikácia na train aj test
train_clean <- clean_data(train)
test_clean  <- clean_data(test)

# uloženie (voliteľné)
# write_csv(train_clean, "train_clean.csv")
# write_csv(test_clean, "test_clean.csv")


