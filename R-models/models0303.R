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
data <- read.csv("/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/3digits_year_country.csv")

# Additional variables
data$age_squared <- data$age^2
data$thinc_log <- log(data$thinc + 1e-8)

data$cell1 <- paste(data$country, data$gender, sep = "_")
cells_to_remove <- data %>% group_by(cell1) %>% summarise(count = n(), .groups = 'drop') %>% filter(count < 2) %>% pull(cell1)
data <- data %>% filter(!(cell1 %in% cells_to_remove))

# Subsets for genders
dataf <- subset(data,gender==1)
datam <- subset(data,gender==0)

# DID variables
data$post = ifelse(data$year >= 2015, 1, 0)
data$treated <- ifelse(data$work_horizon_change_minimum > 0, 1, 0)
data$did <- data$post * data$treated

# Formula
full_formula <- reformulate(c("did","post","treated", "gender","partnerinhh", "nb_children", "nb_grandchildren", "yrseducation", "sphus", "chronic",
                              "life_insurance", "investment", "thinc_log", "jqi_physical_environment", "jqi_social_environment",
                              "jqi_intensity", "jqi_prospects", "jqi_working_time_quality", "jqi_skills_discretion"),response="eurod")
noind_formula <- reformulate(c("did","post","treated", "partnerinhh", "nb_children", "nb_grandchildren", "yrseducation", "sphus", "chronic",
                              "life_insurance", "investment", "thinc_log", "jqi_physical_environment", "jqi_social_environment",
                              "jqi_intensity", "jqi_prospects", "jqi_working_time_quality", "jqi_skills_discretion"),response="eurod")

did_full <- lm(full_formula, data=data, weights=cciw)

did_skills_high = lm(full_formula, data = subset(data, jqi_skills_discretion >= mean(jqi_skills_discretion)+sd(jqi_skills_discretion)), weights = cciw)
did_skills_low= lm(full_formula, data = subset(data, jqi_skills_discretion <= mean(jqi_skills_discretion)-sd(jqi_skills_discretion)), weights = cciw)

did_physical_high = lm(full_formula, data = subset(data, jqi_physical_environment >= mean(jqi_physical_environment)+sd(jqi_physical_environment)), weights = cciw)
did_physical_low= lm(full_formula, data = subset(data, jqi_physical_environment <= mean(jqi_physical_environment)-sd(jqi_physical_environment)), weights = cciw)

did_social_high = lm(full_formula, data = subset(data, jqi_social_environment >= mean(jqi_social_environment)+sd(jqi_social_environment)), weights = cciw)
did_social_low= lm(full_formula, data = subset(data, jqi_social_environment <= mean(jqi_social_environment)-sd(jqi_social_environment)), weights = cciw)

did_time_high = lm(full_formula, data = subset(data, jqi_working_time_quality >= mean(jqi_working_time_quality)+sd(jqi_working_time_quality)), weights = cciw)
did_time_low= lm(full_formula, data = subset(data, jqi_working_time_quality <= mean(jqi_working_time_quality)-sd(jqi_working_time_quality)), weights = cciw)

did_intensity_high = lm(full_formula, data = subset(data, jqi_intensity_slim >= mean(jqi_intensity_slim)+sd(jqi_intensity_slim)), weights = cciw)
did_intensity_low= lm(full_formula, data = subset(data, jqi_intensity_slim <= mean(jqi_intensity_slim)-sd(jqi_intensity_slim)), weights = cciw)

did_prospects_high = lm(full_formula, data = subset(data, jqi_prospects >= mean(jqi_prospects)+sd(jqi_prospects)), weights = cciw)
did_prospects_low= lm(full_formula, data = subset(data, jqi_prospects <= mean(jqi_prospects)-sd(jqi_prospects)), weights = cciw)

# DID female/male
did_female = lm(noind_formula, data = subset(data, gender == 1), weights = cciw)
did_male = lm(noind_formula, data = subset(data, gender == 0), weights = cciw)

# DID female/male jqi_skills_discretion above/below mean
did_female_skills_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_skills_discretion >= mean(jqi_skills_discretion)+sd(jqi_skills_discretion)), weights = cciw)
did_female_skills_low= lm(noind_formula, data = subset(data, gender == 1 & jqi_skills_discretion <= mean(jqi_skills_discretion)-sd(jqi_skills_discretion)), weights = cciw)
did_male_skills_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_skills_discretion >= mean(jqi_skills_discretion)+sd(jqi_skills_discretion)), weights = cciw)
did_male_skills_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_skills_discretion <= mean(jqi_skills_discretion)-sd(jqi_skills_discretion)), weights = cciw)

# DID female/male jqi_physical_environment above/below mean
did_female_physical_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_physical_environment >= mean(jqi_physical_environment)+sd(jqi_physical_environment)), weights = cciw)
did_female_physical_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_physical_environment <= mean(jqi_physical_environment)-sd(jqi_physical_environment)), weights = cciw)
did_male_physical_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_physical_environment >= mean(jqi_physical_environment)+sd(jqi_physical_environment)), weights = cciw)
did_male_physical_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_physical_environment <= mean(jqi_physical_environment)-sd(jqi_physical_environment)), weights = cciw)

# DID female/male jqi_social_environment above/below mean
did_female_social_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_social_environment >= mean(jqi_social_environment)+sd(jqi_social_environment)), weights = cciw)
did_female_social_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_social_environment <= mean(jqi_social_environment)-sd(jqi_social_environment)), weights = cciw)
did_male_social_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_social_environment >= mean(jqi_social_environment)+sd(jqi_social_environment)), weights = cciw)
did_male_social_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_social_environment <= mean(jqi_social_environment)-sd(jqi_social_environment)), weights = cciw)

# DID female/male jqi_working_time_quality above/below mean
did_female_time_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_working_time_quality >= mean(jqi_working_time_quality)+sd(jqi_working_time_quality)), weights = cciw)
did_female_time_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_working_time_quality <= mean(jqi_working_time_quality)-sd(jqi_working_time_quality)), weights = cciw)
did_male_time_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_working_time_quality >= mean(jqi_working_time_quality)+sd(jqi_working_time_quality)), weights = cciw)
did_male_time_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_working_time_quality <= mean(jqi_working_time_quality)-sd(jqi_working_time_quality)), weights = cciw)

# DID female/male jqi_prospects above/below mean
did_female_prospects_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_prospects >= mean(jqi_prospects)+sd(jqi_prospects)), weights = cciw)
did_female_prospects_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_prospects <= mean(jqi_prospects)-sd(jqi_prospects)), weights = cciw)
did_male_prospects_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_prospects >= mean(jqi_prospects)+sd(jqi_prospects)), weights = cciw)
did_male_prospects_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_prospects <= mean(jqi_prospects)-sd(jqi_prospects)), weights = cciw)

# DID female/male jqi_intensity above/below mean
did_female_intensity_high = lm(noind_formula, data = subset(data, gender == 1 & jqi_intensity_slim >= mean(jqi_intensity_slim)+sd(jqi_intensity_slim)), weights = cciw)
did_female_intensity_low = lm(noind_formula, data = subset(data, gender == 1 & jqi_intensity_slim <= mean(jqi_intensity_slim)-sd(jqi_intensity_slim)), weights = cciw)
did_male_intensity_high = lm(noind_formula, data = subset(data, gender == 0 & jqi_intensity_slim >= mean(jqi_intensity_slim)+sd(jqi_intensity_slim)), weights = cciw)
did_male_intensity_low = lm(noind_formula, data = subset(data, gender == 0 & jqi_intensity_slim <= mean(jqi_intensity_slim)-sd(jqi_intensity_slim)), weights = cciw)

summary(did_physical_low, robust = "vcovHC")$coefficients['did',]


# Compare coefficients between models for equality
library(paramhetero)
compare_coefs(model_list =  list(did_physical_high, did_physical_low), padj='none')

# Visualisation
my_data <- data.frame(
  model = c("Skills and discretion", "Skills and discretion", "Physical environment", "Physical environment",
            "Social environment", "Social environment", "Working time quality", "Working time quality",
            "Intensity", "Intensity", "Prospects", "Prospects"),
  var = c("Low", "High", "Low", "High", "Low","High", "Low",
          "High", "Low","High", "Low","High"),
  value = c(-0.423, -0.824, 1.333, -0.473, 0.143, 0.348, 1.451, -0.435, 0.264, -1.177, 0.348, -1.852),
  ci_upper = c(-0.423+0.724, -0.824+0.619, 1.333+0.644, -0.473+0.660,
               0.143+0.525,  0.348+0.706, 1.451+0.720, -0.435+0.347,
               0.264+0.382, -1.177+0.639, 0.348+0.575, -1.852+0.812),
  ci_lower = c(-0.423-0.724, -0.824-0.619, 1.333-0.644, -0.473-0.660,
               0.143-0.525,  0.348-0.706, 1.451-0.720, -0.435-0.347,
               0.264-0.382, -1.177-0.639, 0.348-0.575, -1.852-0.812)
)

  my_colors <- c("High" = "darkgray", "Low" = "darkblue")

  ggplot(my_data, aes(x = model, y = value, color = var)) +
    geom_point(position = position_dodge(0.5)) +
    geom_errorbar(aes(ymin = ci_lower,
                      ymax = ci_upper),
                  width = 0.2, position = position_dodge(0.5)) +
    geom_text(aes(label = round(value, 2)),
              position = position_dodge(0.5),
              vjust = -0.3, hjust = -0.2, size = 3) +
    ggtitle("Effect of ΔYTR on Euro-D for males") +
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

  my_data <- data.frame(
    model = c("Skills and discretion", "Skills and discretion", "Physical environment", "Physical environment",
              "Social environment", "Social environment", "Working time quality", "Working time quality",
              "Intensity", "Intensity", "Prospects", "Prospects"),
    var = c("Low", "High", "Low", "High", "Low","High", "Low",
            "High", "Low","High", "Low","High"),
    value = c(1.554, 1.944, 1.567, 0.752, 1.464, 1.080, 0.823, 0.839, 1.474, 1.287, 1.492, 1.135),
    ci_upper = c(1.554+0.927, 1.944+0.692, 1.567+0.543, 0.752+0.692,
                 1.464+0.293,  1.080+0.586, 0.823+0.529, 0.839+0.792,
                 1.474+0.468, 1.287+0.759, 1.492+0.746, 1.135+0.570),
    ci_lower = c(1.554-0.927, 1.944-0.692, 1.567-0.543, 0.752-0.692,
                 1.464-0.293,  1.080-0.586, 0.823-0.529, 0.839-0.792,
                 1.474-0.468, 1.287-0.759, 1.492-0.746, 1.135-0.570)
  )

  my_colors <- c("High" = "darkgray", "Low" = "darkblue")

  ggplot(my_data, aes(x = model, y = value, color = var)) +
    geom_point(position = position_dodge(0.5)) +
    geom_errorbar(aes(ymin = ci_lower,
                      ymax = ci_upper),
                  width = 0.2, position = position_dodge(0.5)) +
    geom_text(aes(label = round(value, 2)),
              position = position_dodge(0.5),
              vjust = -0.3, hjust = -0.2, size = 3) +
    ggtitle("Effect of ΔYTR on Euro-D for females") +
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
