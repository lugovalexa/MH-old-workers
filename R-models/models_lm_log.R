# Models - LM
# Libraries
library(plm)
library(lmtest)
library(dplyr)
library(crosstable)
library(did)
library(car)
library(corrplot)
library(ggplot2)
library(glmnet)
library(MASS)
library(texreg)
library(sandwich)
library(fixest)

# Data
data <- read.csv("/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/4digits_year.csv")

# Additional variables
data$age_squared <- data$age^2
data$thinc_log <- log(data$thinc + 1e-8)
data$eurod_log <- log(data$eurod + 1e-8)

data$post = ifelse(data$year >= 2015, 1, 0)
data$treated0 <- ifelse(data$work_horizon_change > 0, 1, 0)
data$treated1 <- ifelse(data$work_horizon_change > 1, 1, 0)
data$treated2 <- ifelse(data$work_horizon_change >= 2, 1, 0)

# Cell
data$cell1 <- paste(data$country, data$gender, sep = "_")

data$cell2 <- paste(data$country, data$work_horizon_change, sep = "_")
cells_to_remove <- data %>% group_by(cell2) %>% summarise(count = n(), .groups = 'drop') %>% filter(count < 4) %>% pull(cell2)
data <- data %>% filter(!(cell2 %in% cells_to_remove))

# Subsets for genders
dataf <- subset(data,gender==1)
datam <- subset(data,gender==0)

# Basic model
fit1 <- lm(eurod_log ~ post*treated0, data=data, weights=my_wgt)
summary(fit1, robust = "vcovHC")

# Model with cell fixed effects
fit2 <- lm(eurod_log ~ post*treated0 + as.factor(cell1), data=data, weights=my_wgt)
summary(fit2, robust = "vcovHC")

# Full model without all indexes
fit3 <- lm(eurod_log ~ post*treated0 + partnerinhh + nb_children + nb_grandchildren + yrseducation + sphus + chronic
           + life_insurance + investment + thinc_log + work_horizon + jqi_sum + as.factor(cell2) + as.factor(industry),
           data=data, weights=my_wgt)
summary(fit3, robust = "vcovHC")

# Full model
fit4 <- lm(eurod_log ~ post*treated0 + partnerinhh + nb_children + nb_grandchildren + yrseducation + sphus + chronic
           + life_insurance + investment + thinc_log + work_horizon + jqi_physical_environment + jqi_social_environment
           + jqi_intensity + jqi_prospects + jqi_working_time_quality + as.factor(cell2) + as.factor(industry),
           data=data, weights=my_wgt)
summary(fit4, robust = "vcovHC")$coefficients['post:treated0',]


# Clustered errors
clustered_se <- vcovHC(fit1, type = "HC1", cluster = "cell1")
robust_se <- sqrt(diag(clustered_se))
coeftest(fit1, vcov. = clustered_se)

# Formula
interaction_formula <- paste(interaction_terms_colnames, collapse = " + ")
full_formula <- reformulate(c("post*treated0", "partnerinhh", "nb_children", "nb_grandchildren", "yrseducation", "sphus", "chronic",
                              "life_insurance", "investment", "thinc_log", "work_horizon", "jqi_physical_environment", "jqi_social_environment",
                              "jqi_intensity", "jqi_prospects", "jqi_working_time_quality", "as.factor(cell2)", "as.factor(industry)"),response="eurod_log")
noind_formula <- reformulate(c("post*treated0", "partnerinhh", "nb_children", "nb_grandchildren", "yrseducation", "sphus", "chronic",
                               "life_insurance", "investment", "thinc_log", "work_horizon", "jqi_sum", "as.factor(cell2)", "as.factor(industry)"),response="eurod_log")

# DID female/male
did_female = lm(full_formula, data = subset(data, gender == 1), weights = my_wgt)
did_male = lm(full_formula, data = subset(data, gender == 0), weights = my_wgt)

# DID female/male jqi_skills_discretion above/below mean
did_female_skills_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_skills_discretion >= median(jqi_skills_discretion)), weights = my_wgt)
did_female_skills_low= lm(noind_formula, data = subset(data, gender == 1 & jqi_skills_discretion < median(jqi_skills_discretion)), weights = my_wgt)
did_male_skills_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_skills_discretion >= median(jqi_skills_discretion)), weights = my_wgt)
did_male_skills_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_skills_discretion < median(jqi_skills_discretion)), weights = my_wgt)

# DID female/male jqi_physical_environment above/below mean
did_female_physical_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_physical_environment >= median(jqi_physical_environment)), weights = my_wgt)
did_female_physical_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_physical_environment < median(jqi_physical_environment)), weights = my_wgt)
did_male_physical_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_physical_environment >= median(jqi_physical_environment)), weights = my_wgt)
did_male_physical_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_physical_environment < median(jqi_physical_environment)), weights = my_wgt)

# DID female/male jqi_social_environment above/below mean
did_female_social_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_social_environment >= median(jqi_social_environment)), weights = my_wgt)
did_female_social_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_social_environment < median(jqi_social_environment)), weights = my_wgt)
did_male_social_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_social_environment >= median(jqi_social_environment)), weights = my_wgt)
did_male_social_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_social_environment < median(jqi_social_environment)), weights = my_wgt)

# DID female/male jqi_working_time_quality above/below mean
did_female_time_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_working_time_quality >= median(jqi_working_time_quality)), weights = my_wgt)
did_female_time_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_working_time_quality < median(jqi_working_time_quality)), weights = my_wgt)
did_male_time_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_working_time_quality >= median(jqi_working_time_quality)), weights = my_wgt)
did_male_time_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_working_time_quality < median(jqi_working_time_quality)), weights = my_wgt)

# DID female/male jqi_prospects above/below mean
did_female_prospects_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_prospects >= median(jqi_prospects)), weights = my_wgt)
did_female_prospects_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_prospects < median(jqi_prospects)), weights = my_wgt)
did_male_prospects_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_prospects >= median(jqi_prospects)), weights = my_wgt)
did_male_prospects_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_prospects < median(jqi_prospects)), weights = my_wgt)

# DID female/male jqi_intensity above/below mean
did_female_intensity_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_intensity >= median(jqi_intensity)), weights = my_wgt)
did_female_intensity_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_intensity < median(jqi_intensity)), weights = my_wgt)
did_male_intensity_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_intensity >= median(jqi_intensity)), weights = my_wgt)
did_male_intensity_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_intensity < median(jqi_intensity)), weights = my_wgt)

summary(did_male_intensity_low, robust = "vcovHC")$coefficients['post:treated0',]
