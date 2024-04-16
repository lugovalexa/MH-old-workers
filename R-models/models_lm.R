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
data <- read.csv("/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/4digits_country.csv")

# Additional variables
data$age_squared <- data$age^2
data$thinc_log <- log(data$thinc + 1e-8)
data$eurod_log <- log(data$eurod + 1e-8)

data$post = ifelse(data$year >= 2015, 1, 0)
data$treated0 <- ifelse(data$work_horizon_change_minimum > 0, 1, 0)
data$treated1 <- ifelse(data$work_horizon_change_minimum > 1, 1, 0)
data$treated2 <- ifelse(data$work_horizon_change_minimum >= 2, 1, 0)

# Cell
data$cell1 <- paste(data$country, data$gender, sep = "_")

data$cell2 <- paste(data$country, data$work_horizon_change_minimum, sep = "_")
cells_to_remove <- data %>% group_by(cell2) %>% summarise(count = n(), .groups = 'drop') %>% filter(count < 4) %>% pull(cell2)
data <- data %>% filter(!(cell2 %in% cells_to_remove))

# Subsets for genders
dataf <- subset(data,gender=="Female")
datam <- subset(data,gender=="Male")

# Basic model
fit1 <- lm(eurod ~ post*treated0, data=data, weights=cciw)
summary(fit1, robust = "vcovHC")

# Model with cell fixed effects
fit2 <- lm(eurod ~ post*treated0 + as.factor(cell1), data=data, weights=cciw)
summary(fit2, robust = "vcovHC")

# Full model without all indexes
fit3 <- lm(eurod ~ post*treated2 + partnerinhh + nb_children + nb_grandchildren + yrseducation + sphus + chronic
           + life_insurance + investment + thinc_log + work_horizon + jqi_sum + as.factor(cell1) + as.factor(industry),
           data=datam, weights=cciw)
summary(fit3, robust = "vcovHC")

# Full model
fit4 <- lm(eurod ~ post*treated0 + as.factor(gender) + partnerinhh + nb_children + nb_grandchildren + yrseducation + sphus + chronic
            + life_insurance + investment + thinc_log + work_horizon + jqi_physical_environment + jqi_social_environment
            + jqi_intensity + jqi_prospects + jqi_working_time_quality + jqi_skills_discretion + as.factor(cell1) + as.factor(industry),
            data=subset(dataf,jqi_physical_environment > median(jqi_physical_environment)), weights=cciw)
summary(fit4, robust = "vcovHC")$coefficients['post:treated0',]

# Clustered errors
clustered_se <- vcovHC(fit1, type = "HC1", cluster = "cell1")
robust_se <- sqrt(diag(clustered_se))
coeftest(fit1, vcov. = clustered_se)

# Formula
interaction_formula <- paste(interaction_terms_colnames, collapse = " + ")
full_formula <- reformulate(c("post*treated1", "gender","partnerinhh", "nb_children", "nb_grandchildren", "yrseducation", "sphus", "chronic",
                              "life_insurance", "investment", "thinc_log", "work_horizon", "jqi_physical_environment", "jqi_social_environment",
                              "jqi_intensity", "jqi_prospects", "jqi_working_time_quality", "jqi_skills_discretion", "as.factor(cell2)", "as.factor(industry)"),response="eurodcat")
noind_formula <- reformulate(c("post*treated1", "partnerinhh", "nb_children", "nb_grandchildren", "yrseducation", "sphus", "chronic",
                               "life_insurance", "investment", "thinc_log", "work_horizon", "jqi_physical_environment", "jqi_social_environment",
                               "jqi_intensity", "jqi_prospects", "jqi_working_time_quality",  "jqi_skills_discretion", "as.factor(cell2)", "as.factor(industry)"),response="eurodcat")

full_formula <- reformulate(c("post*treated0", "as.factor(cell1)"),response="eurod")
noind_formula <- reformulate(c("post*treated0", "as.factor(cell1)"),response="eurod")

did_full <- lm(full_formula, data=data, weights=my_wgt)

did_skills_high = lm(full_formula, data = subset(data, jqi_skills_discretion > median(jqi_skills_discretion)), weights = my_wgt)
did_skills_low= lm(full_formula, data = subset(data, jqi_skills_discretion < median(jqi_skills_discretion)), weights = my_wgt)

did_physical_high = lm(full_formula, data = subset(data, jqi_physical_environment > median(jqi_physical_environment)), weights = my_wgt)
did_physical_low= lm(full_formula, data = subset(data, jqi_physical_environment < median(jqi_physical_environment)), weights = my_wgt)

did_social_high = lm(full_formula, data = subset(data, jqi_social_environment > median(jqi_social_environment)), weights = my_wgt)
did_social_low= lm(full_formula, data = subset(data, jqi_social_environment < median(jqi_social_environment)), weights = my_wgt)

did_time_high = lm(full_formula, data = subset(data, jqi_working_time_quality > median(jqi_working_time_quality)), weights = my_wgt)
did_time_low= lm(full_formula, data = subset(data, jqi_working_time_quality < median(jqi_working_time_quality)), weights = my_wgt)

did_intensity_high = lm(full_formula, data = subset(data, jqi_intensity > median(jqi_intensity)), weights = my_wgt)
did_intensity_low= lm(full_formula, data = subset(data, jqi_intensity < median(jqi_intensity)), weights = my_wgt)

did_prospects_high = lm(full_formula, data = subset(data, jqi_prospects > median(jqi_prospects)), weights = my_wgt)
did_prospects_low= lm(full_formula, data = subset(data, jqi_prospects < median(jqi_prospects)), weights = my_wgt)

# DID female/male
did_female = lm(noind_formula, data = subset(data, gender == 1), weights = my_wgt)
did_male = lm(noind_formula, data = subset(data, gender == 0), weights = my_wgt)

# DID female/male jqi_skills_discretion above/below mean
did_female_skills_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_skills_discretion > median(jqi_skills_discretion)), weights = my_wgt)
did_female_skills_low= lm(noind_formula, data = subset(data, gender == 1 & jqi_skills_discretion < median(jqi_skills_discretion)), weights = my_wgt)
did_male_skills_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_skills_discretion > median(jqi_skills_discretion)), weights = my_wgt)
did_male_skills_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_skills_discretion < median(jqi_skills_discretion)), weights = my_wgt)

# DID female/male jqi_physical_environment above/below mean
did_female_physical_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_physical_environment > median(jqi_physical_environment)), weights = my_wgt)
did_female_physical_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_physical_environment < median(jqi_physical_environment)), weights = my_wgt)
did_male_physical_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_physical_environment > median(jqi_physical_environment)), weights = my_wgt)
did_male_physical_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_physical_environment < median(jqi_physical_environment)), weights = my_wgt)

# DID female/male jqi_social_environment above/below mean
did_female_social_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_social_environment > median(jqi_social_environment)), weights = my_wgt)
did_female_social_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_social_environment < median(jqi_social_environment)), weights = my_wgt)
did_male_social_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_social_environment > median(jqi_social_environment)), weights = my_wgt)
did_male_social_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_social_environment < median(jqi_social_environment)), weights = my_wgt)

# DID female/male jqi_working_time_quality above/below mean
did_female_time_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_working_time_quality > median(jqi_working_time_quality)), weights = my_wgt)
did_female_time_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_working_time_quality < median(jqi_working_time_quality)), weights = my_wgt)
did_male_time_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_working_time_quality > median(jqi_working_time_quality)), weights = my_wgt)
did_male_time_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_working_time_quality < median(jqi_working_time_quality)), weights = my_wgt)

# DID female/male jqi_prospects above/below mean
did_female_prospects_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_prospects > median(jqi_prospects)), weights = my_wgt)
did_female_prospects_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_prospects < median(jqi_prospects)), weights = my_wgt)
did_male_prospects_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_prospects > median(jqi_prospects)), weights = my_wgt)
did_male_prospects_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_prospects < median(jqi_prospects)), weights = my_wgt)

# DID female/male jqi_intensity above/below mean
did_female_intensity_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_intensity > median(jqi_intensity)), weights = my_wgt)
did_female_intensity_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_intensity < median(jqi_intensity)), weights = my_wgt)
did_male_intensity_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_intensity > median(jqi_intensity)), weights = my_wgt)
did_male_intensity_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_intensity < median(jqi_intensity)), weights = my_wgt)

summary(did_female_prospects_low, robust = "vcovHC")$coefficients['post:treated0',]

# compare coefficients between models for equality
library(paramhetero)
compare_coefs(model_list =  list(did_female_prospects_high, did_female_prospects_low), padj='none')

# visualisation
my_data <- data.frame(
  model = c("Skills and discretion", "Skills and discretion", "Physical environment", "Physical environment",
            "Social environment", "Social environment", "Working time quality", "Working time quality",
            "Intensity", "Intensity", "Prospects", "Prospects"),
  var = c("Above 75th percentile", "Below 25th percentile", "Above 75th percentile", "Below 25th percentile","Above 75th percentile", "Below 25th percentile",
          "Above 75th percentile", "Below 25th percentile","Above 75th percentile", "Below 25th percentile","Above 75th percentile", "Below 25th percentile"),
  value = c(-0.058, 0.166, -0.076, 0.612, -0.055, 0.067, 0.026, 0.626, -0.121, 0.611, -0.204, 0.385),
  ci_upper = c(-0.058+0.231, 0.166+0.227, -0.076+0.153, 0.612+0.296,
               -0.055+0.140, 0.067+0.149, 0.026+0.319, 0.626+0.257,
               -0.121+0.254, 0.611+0.269, -0.204+0.405, 0.385+0.248),
  ci_lower = c(-0.058-0.231, 0.166-0.227, -0.076-0.153, 0.612-0.296,
               -0.055-0.140, 0.067-0.149, 0.026-0.319, 0.626-0.257,
               -0.121-0.254, 0.611-0.269, -0.204-0.405, 0.385-0.248)
)

my_colors <- c("Above 75th percentile" = "darkgray", "Below 25th percentile" = "darkblue")

ggplot(my_data, aes(x = model, y = value, color = var)) +
  geom_point(position = position_dodge(0.5)) +
  geom_errorbar(aes(ymin = ci_lower,
                    ymax = ci_upper),
                width = 0.2, position = position_dodge(0.5)) +
  geom_text(aes(label = round(value, 2)),
            position = position_dodge(0.5),
            vjust = -0.3, hjust = -0.2, size = 3) +
  labs(x = "Job Quality Index",
       y = "Effect of ΔYTR on Euro-D (0-12)") +
  theme_light() +
  scale_color_manual(values = my_colors) +
  facet_wrap(~model, scales = "free_x") +
  theme(axis.text.x = element_blank()) +
  theme(
    strip.background = element_rect(fill = "darkblue"),
    strip.text = element_text(color = "white")
  )
