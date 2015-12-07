#Transform the sample data so that it can be added to the db
library(random)
library(plyr)
library(dplyr)

bid <- read.delim("/Users/Administrator/Desktop/COMPSCI316/AmazonVM/Project/sample_R/bid.txt", stringsAsFactors=FALSE)
book <- read.delim("/Users/Administrator/Desktop/COMPSCI316/AmazonVM/Project/sample_R/book.txt", comment.char="#", stringsAsFactors=FALSE)
listing <- read.delim("/Users/Administrator/Desktop/COMPSCI316/AmazonVM/Project/sample_R/listing.txt", stringsAsFactors=FALSE)
user <- read.csv("/Users/Administrator/Desktop/COMPSCI316/AmazonVM/Project/sample_R/user_raw.csv", stringsAsFactors=FALSE)

listing$id = 1:nrow(listing)
listing$is_auction = listing$is_auction == 1
listing$is_buy_it_now = listing$is_buy_it_now == 1
listing$active = T




# for (i in 1:nrow(book)){
#   f = round(10*runif(1)) + 1
#   first_name = randomStrings(1, f, digits = F, upperalpha = F)
#   last_name = randomStrings(1, f, digits = F, upperalpha = F)
#   book$first_author_name[i] = paste(first_name, last_name, sep = " ")
# }

bid$id = 1:nrow(bid)
bid = merge(bid, listing, by.x = c("book_ISBN", "listing_start_time", "seller_email"), 
            by.y = c("book_ISBN", "start_time", "seller_email"))

bid = plyr::rename(bid, replace = c(book_ISBN = "book_id", id.y = "listing_id", id.x = "id"))
listing = plyr::rename(listing, replace = c(book_ISBN = "book_id", start_price = "start_bid"))

listing$condition[listing$condition == "Likenew"] <- "excellent"
listing$condition[listing$condition == "Used"] <- "Fair"

bidMax = aggregate(bid_price ~ listing_id, data = bid, max)

bid = merge(bid, bidMax, by = c("bid_price", "listing_id"))
bidVars = c("id","bid_time", "bid_price", "bidder_email", "listing_id")
bid = bid[bidVars]

#listing = merge(listing, bid, by.x = "id", by.y = "listing_id", all.x = TRUE)
#listing = plyr::rename(listing, replace(bid_price = "current_bid"))
listingVars = c("id", "start_time", "condition", "is_auction", "is_buy_it_now", "description", 
                "buy_it_now_price", "seller_email", "start_bid", "active", "title", "book_id")
listing = listing[listingVars]

book <- subset(book, !duplicated(book$ISBN) )
book$second_author_name = book$third_author_name = book$fourth_author_name = book$fifth_author_name = ""
book = plyr::rename(book, replace = c(author = "first_author_name"))
bookVars = c("ISBN", "edition", "title", "fifth_author_name", "fourth_author_name", "second_author_name",
             "first_author_name", "third_author_name")
book = book[bookVars]
book$first_author_name = iconv(book$first_author_name, from="latin1", to = "ASCII", sub = "")


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


userVars = c("id", "password", "last_login", "is_superuser", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined", "username")
user = user[userVars]

listingKeep = c("id", "start_time", "condition", "is_auction", "is_buy_it_now", "description", 
                "buy_it_now_price", "seller_email", "start_bid", "active", "book_id")
listing = listing[listingKeep]
listing = listing[1:1038,]


#listing_book = merge(listing, book, by.x = c("book_id","title"), by.y = c("ISBN","title"), all.x = TRUE)
#listing_book = plyr::rename(listing_book, replace = c(book_id = "isbn"))
#listing_book_Keep = c("id", "start_time", "condition", "is_auction", "is_buy_it_now", "description", "buy_it_now_price", "seller_email", "start_bid", "active", "edition", "fifth_author_name", "first_author_name", "fourth_author_name", "isbn", "second_author_name", "third_author_name", "title")


#listing_book = listing_book[listing_book_Keep]

write.table(bid, "/Users/Administrator/Desktop/COMPSCI316/AmazonVM/Project/sample_R_output/bid.csv", row.names=FALSE, col.names=FALSE, sep=",")
write.table(book, "/Users/Administrator/Desktop/COMPSCI316/AmazonVM/Project/sample_R_output/book.csv", row.names=FALSE, col.names=FALSE, sep=",")
write.table(listing, "/Users/Administrator/Desktop/COMPSCI316/AmazonVM/Project/sample_R_output/listing.csv", row.names=FALSE, col.names=FALSE, sep=",")
write.table(user, "/Users/Administrator/Desktop/COMPSCI316/AmazonVM/Project/sample_R_output/user.csv", row.names=FALSE, col.names=FALSE, sep=",")