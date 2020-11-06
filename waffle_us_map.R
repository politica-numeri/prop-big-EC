library(tidyverse)
#install.packages("remotes")
#remotes::install_github("hrbrmstr/waffle")
library(waffle)

ec_seats <- read_delim("ec-seats.txt", "\t", escape_double = FALSE, trim_ws = TRUE)

ec_seats_longer <- ec_seats %>% pivot_longer(Biden:Duncan, "candidate", values_to = "ev") %>% select(-X30) %>%
  group_by(candidate) %>% mutate(perc = prop.table(ev))

ec_seats_summarised <- ec_seats %>% pivot_longer(Biden:Duncan, "candidate", values_to = "ev") %>% select(-X30) %>%
  group_by(candidate) %>% mutate(perc = prop.table(ev)) %>%
  summarise(ev = sum(ev)) %>% filter(ev > 0)

colors = c("Biden" = "blue",
           "De La Fuente" = "purple",
           "Hawkins" = "green",
           "Jorgensen" = "gold",
           "La Riva" = "darkred",
           "Pierce" = "steelblue",
           "Trump" = "red")

ec_seats_summarised %>% ggplot(aes(fill = factor(candidate), values = ev)) +
  geom_waffle(color = "white", n_rows = 75) + coord_equal() +
  scale_fill_manual(values = colors) +
  theme_void() + labs(fill = "candidate")
ggsave("waffleus.pdf", scale = 3)


ec_seats_longer %>% ggplot(aes(fill = factor(candidate), values = ev)) + geom_waffle(color = "white", n_rows = 25, alpha = 0.9) + scale_fill_manual(values = colors) +
  facet_wrap(~State, ncol = 5, scales = "free") + theme_void() + labs(fill = "candidate")
ggsave("waffle2.pdf", scale = 3)
