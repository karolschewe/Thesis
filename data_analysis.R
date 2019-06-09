library(VGAM)
# wczytanie danych
this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

part1<-read.csv("gminy1.csv")
part2<-read.csv("gminy2.csv")
part3<-read.csv("gminy3.csv")
part4<-read.csv("gminy4.csv")

df<-rbind(part1,part2,part3,part4)

# usuwanie duplikatów
df.data<-unique(df)
df.data<-df.data[df.data$pm10>0,]

# dodanie kolumny z pierwszymi dwoma cyframi kodu pocztowego

df.data$post_id<-factor(substr(as.character(df.data$kod_pocztowy),1,2))

# srednie zakurzenie po wojewodztwach
po.wojewodztwach<-aggregate(pm10 ~ wojewodztwo, df.data, mean)

po.wojewodztwach.desc <- po.wojewodztwach[with(po.wojewodztwach, order(-pm10)), ]

# dopasowanie:
x <- log(2:17)
y <- log(po.wojewodztwach.desc$pm10)
xy.lm <- lm(y ~ x)
summary(xy.lm)

b <- xy.lm$coefficients[1]
a <- xy.lm$coefficients[2]
plot(x, y, pch=19, main = "Sprawdzenie prawa Zipfa dla hierarchii stezen PM10 wedlug wojewodztw",xlab = "log(ranga)",ylab="log(PM10)")
lines(x, a*x+b, col="red", lwd=3)

woj.pval<-chisq.test(y, p = (a*x+b)/sum(a*x+b))

# srednie zakurzenie po gminach
po.gminach<-aggregate(pm10 ~ gmina, df.data, mean)
po.gminach.desc <- po.gminach[with(po.gminach, order(-pm10)), ]

# dopasowanie:
x <- log(2:(length(po.gminach.desc$pm10)+1))
y <- log(po.gminach.desc$pm10)
xy.lm <- lm(y ~ x)
summary(xy.lm)

b <- xy.lm$coefficients[1]
a <- xy.lm$coefficients[2]
plot(x, y, pch=19, main = "Sprawdzenie prawa Zipfa dla hierarchii stezen PM10 wedlug gmin",xlab = "log(ranga)",ylab="log(PM10)")
lines(x, a*x+b, col="red", lwd=3)

gm.pval<-chisq.test(y, p = (a*x+b)/sum(a*x+b))

# srednie zakurzenie po sensorach
po.sensorach<-aggregate(pm10 ~ id, df.data, mean)
po.sensorach.desc <- po.sensorach[with(po.sensorach, order(-pm10)), ]


# dopasowanie:
x <- log(2:(length(po.sensorach.desc$pm10)+1))
y <- log(po.sensorach.desc$pm10)
xy.lm <- lm(y ~ x)
summary(xy.lm)

b <- xy.lm$coefficients[1]
a <- xy.lm$coefficients[2]
plot(x, y, pch=19, main = "Sprawdzenie prawa Zipfa dla hierarchii stezen PM10 wedlug sensorow",xlab = "log(ranga)",ylab="log(PM10)")
lines(x, a*x+b, col="red", lwd=3)

sensor.pval<-chisq.test(y, p = (a*x+b)/sum(a*x+b))


# srednie zakurzenie po kodach
po.post_id<-aggregate(pm10 ~ post_id, df.data, mean)
po.post_id.desc <- po.post_id[with(po.post_id, order(-pm10)), ]

# dopasowanie:
x <- log(2:(length(po.post_id.desc$pm10)+1))
y <- log(po.post_id.desc$pm10)
plot(x, y)
xy.lm <- lm(y ~ x)
summary(xy.lm)

b <- xy.lm$coefficients[1]
a <- xy.lm$coefficients[2]
plot(x, y, pch=19, main = "Sprawdzenie prawa Zipfa dla hierarchii stezen PM10\n wedlug pierwszych dwóch cyfr kodu pocztowego",xlab = "log(ranga)",ylab="log(PM10)")
lines(x, a*x+b, col="red", lwd=3)


kod.pval<-chisq.test(y, p = (a*x+b)/sum(a*x+b))




