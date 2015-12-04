#Transform the sample data so that it can be added to the db
library(plyr)

bid <- read.csv("~/316/project/sample data/bid.txt", stringsAsFactors=FALSE)
book <- read.csv("~/316/project/sample data/book.txt", comment.char="#", stringsAsFactors=FALSE)
listing <- read.csv("~/316/project/sample data/listing.txt", stringsAsFactors=FALSE)
user <- read.csv("~/316/project/sample data/user_raw.csv", stringsAsFactors=FALSE)

listing$id = 1:nrow(listing)
listing$is_auction = listing$is_auction == 1
listing$is_buy_it_now = listing$is_buy_it_now == 1
listing$active = F


bid$id = 1:nrow(bid)
bid = merge(bid, listing, by.x = c("book_ISBN", "listing_start_time", "seller_email"), 
            by.y = c("book_ISBN", "start_time", "seller_email"))

bid = rename(bid, replace = c(book_ISBN = "book_id", id.y = "listing_id", id.x = "id"))
listing = rename(listing, replace = c(book_ISBN = "book_id", start_price = "start_bid"))
listing$condition[listing$condition == "Likenew"] <- "excellent"
listing$condition[listing$condition == "Used"] <- "Fair"


bidVars = c("id","bid_time", "bid_price", "bidder_email", "listing_id")
bid = bid[bidVars]


listingVars = c("id", "start_time", "condition", "is_auction", "is_buy_it_now", "description", 
                "buy_it_now_price", "seller_email", "start_bid", "active", "current_bid", "book_id")
listing = listing[listingVars]

book <- subset(book, !duplicated(book$ISBN) )
book$second_author_name = book$third_author_name = book$fourth_author_name = book$fifth_author_name = ""
book = rename(book, replace = c(author = "first_author_name"))
bookVars = c("edition", "ISBN", "title", "fifth_author_name", "fourth_author_name", "second_author_name",
             "first_author_name", "third_author_name")
book = book[bookVars]



user$id = 1:nrow(user)
user$password = "123"
user$is_superuser = F
for (i in 1:nrow(user)){
  user$first_name[i] = strsplit(user$name[i], " ")[[1]][1]
  user$last_name[i] = strsplit(user$name[i], " ")[[1]][2]
  user$username[i] = paste0(substr(user$first_name[i],1, 1), user$last_name[i])
  
}

user$is_staff = F
user$is_active = T
user$date_joined = as.POSIXct(Sys.Date() - 10)
user$last_login = as.POSIXct(Sys.Date() - 5)


userVars = c("id", "password", "is_superuser", "username", "first_name", "last_name", "email",
             "is_staff", "is_active", "date_joined", "last_login")

user = user[userVars]

write.table(bid, "~/316/project/sample data/bid.csv", row.names=FALSE, col.names=FALSE, sep=",")
write.table(book, "~/316/project/sample data/book.csv", row.names=FALSE, col.names=FALSE, sep=",")
write.table(listing, "~/316/project/sample data/listing.csv", row.names=FALSE, col.names=FALSE, sep=",")
write.table(user, "~/316/project/sample data/user.csv", row.names=FALSE, col.names=FALSE, sep=",")