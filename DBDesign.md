
---

# Database Design Documentation

## Overview

This database design captures the structure of a system for managing an e-commerce platform, including product management, user accounts, orders, purchases, investments, salaries, and more. The design uses a relational database model.

## Tables

### ProductCategory

- **CategoryID (Primary Key):** Unique identifier for each product category.
- **Title:** Name of the product category.
- **CoverPicture:** URL or path to the cover picture of the category.
- **ProfilePicture:** URL or path to the profile picture of the category.

### ProductDescription

- **DescriptionID (Primary Key):** Unique identifier for each product description.
- **CategoryID (Foreign Key):** Reference to the associated product category.
- **DescriptionTitle:** Title of the product description.
- **DescriptionText:** Textual description of the product.
- **SpecificationText:** Textual specifications of the product.

### ProductSizeChart

- **SizeChartID (Primary Key):** Unique identifier for each product size chart.
- **CategoryID (Foreign Key):** Reference to the associated product category.
- **SizeChart:** JSON data representing the size chart.

### Product

- **ProductID (Primary Key):** Unique identifier for each product.
- **CategoryID (Foreign Key):** Reference to the associated product category.
- **DescriptionID (Foreign Key):** Reference to the associated product description.
- **SizeChartID (Foreign Key):** Reference to the associated product size chart.
- **RealPrice:** Actual price of the product.
- **DiscountPercentage:** Percentage of discount applied.
- **SaleCount:** Number of units sold.
- **visited:** Number of visits to the product page.
- **wishlisted:** Number of times the product is wishlisted.
- **VideoURL:** URL to product video.
- **StoreId (Foreign Key):** Reference to the associated store.

### ProductPhoto

- **PhotoID (Primary Key):** Unique identifier for each product photo.
- **ProductID (Foreign Key):** Reference to the associated product.
- **PhotoURL:** URL or path to the product photo.

### Tag

- **TagID (Primary Key):** Unique identifier for each tag.
- **TagName:** Name of the tag.

### ProductTags

- **ProductTagID (Primary Key):** Unique identifier for each product-tag association.
- **ProductID (Foreign Key):** Reference to the associated product.
- **TagID (Foreign Key):** Reference to the associated tag.

### ProductSizeQuantity

- **SizeQuantityID (Primary Key):** Unique identifier for each product size quantity.
- **ProductID (Foreign Key):** Reference to the associated product.
- **ProductSize:** Size of the product.
- **QuantityInStock:** JSON data representing quantity in stock for each size.

### Review

- **ReviewID (Primary Key):** Unique identifier for each product review.
- **ProductID (Foreign Key):** Reference to the associated product.
- **Rating:** Numeric rating given by the user.
- **Description:** Textual review description.

### Banner

- **BannerId (Primary Key):** Unique identifier for each banner.
- **PhotoURL:** URL or path to the banner photo.
- **BannerURL:** URL or path to the banner link.

### Offer

- **OfferId (Primary Key):** Unique identifier for each offer.
- **OfferType:** Type of offer.
- **OfferTitle:** Title of the offer.
- **OfferDescription:** Description of the offer.
- **CoverPictureURL:** URL or path to the cover picture of the offer.
- **RedirectURL:** URL to redirect when the offer is clicked.
- **NotifyViaSMS:** Boolean indicating whether to notify via SMS.
- **NotifyViaApp:** Boolean indicating whether to notify via the app.
- **NotificationFrequencyHour:** Frequency of notification (hours).
- **SMSFrequencyHour:** Frequency of SMS notification (hours).
- **DurationDay:** Duration of the offer (days).
- **PromoCode:** Promo code for the offer.
- **MinimumPurchase:** Minimum purchase amount for the offer.
- **DiscountPercentage:** Percentage of discount for the offer.
- **ProductList:** JSON data representing the list of products in the offer.

### Notification

- **NotificationId (Primary Key):** Unique identifier for each notification.
- **Title:** Title of the notification.
- **Description:** Description of the notification.
- **CoverPictureURL:** URL or path to the cover picture of the notification.
- **RedirectURL:** URL to redirect when the notification is clicked.
- **NotifyViaSMS:** Boolean indicating whether to notify via SMS.
- **NotifyViaApp:** Boolean indicating whether to notify via the app.
- **NotificationFrequencyHour:** Frequency of notification (hours).
- **SMSFrequencyHour:** Frequency of SMS notification (hours).
- **DurationDay:** Duration of the notification (days).
- **ProductList:** JSON data representing the list of products in the notification.

### User

- **UserId (Primary Key):** Unique identifier for each user.
- **PhoneNo:** Phone number of the user.
- **FullName:** Full name of the user.
- **Address:** Address of the user.
- **Email:** Email address of the user.
- **City:** City of the user.
- **Zone:** Zone of the user.
- **Area:** Area of the user.
- **UserName:** Username of the user.
- **Parchase:** Number of purchases made by the user.
- **Point:** User points.
- **Visit:** Number of visits by the user.
- **IsStaff:** Boolean indicating whether the user is a staff member.
- **StaffLevel:** Level or role of the staff member.
- **CreatedAt:** Timestamp indicating when the user was created.
- **UpdatedAt:** Timestamp indicating when the user was last updated.

### Store

- **StoreId (Primary Key):** Unique identifier for each store.
- **ContactName:** Name of the store contact person.
- **ContactNumber:** Phone number of the store contact person.
- **SecondContactNumber:** Second phone number of the store contact person.
- **StoreAddress:** Address of the store.
- **StoreCity:** City of the store.
- **StoreZone:** Zone of the store.
- **StoreArea:** Area of the store.

### Order

- **OrderID (Primary Key):** Unique identifier for each order.
- **CreatedAt:** Timestamp indicating when the order was created.
- **UpdatedAt:** Timestamp indicating when the order was last updated.
- **CustomerID (Foreign Key):** Reference to the associated user (customer).
- **CustomerName:** Name of the customer.
- **CustomerPhone:** Phone number of the customer.
- **CustomerEmail:** Email address of the customer.
- **CustomerAddress:** Address of the customer.
- **CustomerCity:** City of the customer.
- **CustomerZone:** Zone of the customer.
- **CustomerArea:** Area of the customer.
- **StoreId (Foreign Key):** Reference to the associated store.
- **ProductValue:** Total value of products in the order.
- **OrderValue:** Total value of the order.
- **ItemType:** Type of item in the order.
- **ItemQuantity:** Quantity of items in the order.
- **ItemWeight:** Total weight

 of items in the order.
- **ItemDescription:** Description of the item.
- **DeliveryNote:** Note related to the delivery.
- **DeliveryType:** Type of delivery.
- **DeliveryCost:** Cost of delivery.
- **AmountToCollect:** Amount to collect from the customer.
- **DeliveryConsignmentId:** Consignment ID for delivery.
- **DeliveryTrackingURL:** URL for tracking the delivery.
- **PaymentMethod:** Method of payment.
- **OrderStatus:** Status of the order.
- **PaymentStatus:** Status of payment.
- **Profit:** Profit from the order.

### OrderedProduct

- **Id (Primary Key):** Unique identifier for each ordered product.
- **OrderID (Foreign Key):** Reference to the associated order.
- **ProductID (Foreign Key):** Reference to the associated product.
- **ProductSize:** Size of the ordered product.

### Purchase

- **PurchaseId (Primary Key):** Unique identifier for each purchase.
- **CreatedAt:** Timestamp indicating when the purchase was created.
- **Title:** Title of the purchase.
- **Description:** Description of the purchase.
- **PurchaseAmount:** Amount of the purchase.
- **IsApproved:** Boolean indicating whether the purchase is approved.

### PurchaseApproval

- **PurchaseApprovalId (Primary Key):** Unique identifier for each purchase approval.
- **PurchaseId (Foreign Key):** Reference to the associated purchase.
- **ApproverID (Foreign Key):** Reference to the user who approved the purchase.
- **IsApproved:** Boolean indicating whether the purchase is approved.

### PurchasePhoto

- **PhotoID (Primary Key):** Unique identifier for each purchase photo.
- **PurchaseId (Foreign Key):** Reference to the associated purchase.
- **PhotoURL:** URL or path to the purchase photo.

### AccountBalance

- **AccountBalanceId (Primary Key):** Unique identifier for each account balance.
- **CreatedAt:** Timestamp indicating when the account balance was created.
- **InformerId (Foreign Key):** Reference to the user who informed about the balance.
- **CurrentBalance:** Current balance amount.
- **PictureOfProffURL:** URL or path to the picture of proof.
- **IsApproved:** Boolean indicating whether the account balance is approved.

### AccountBalanceApproval

- **AccountBalanceApprovalId (Primary Key):** Unique identifier for each account balance approval.
- **AccountBalanceId (Foreign Key):** Reference to the associated account balance.
- **ApproverID (Foreign Key):** Reference to the user who approved the account balance.
- **IsApproved:** Boolean indicating whether the account balance is approved.

### Investment

- **InvestmentId (Primary Key):** Unique identifier for each investment.
- **CreatedAt:** Timestamp indicating when the investment was created.
- **InvestorID (Foreign Key):** Reference to the investor user.
- **InvestedAmount:** Amount of the investment.
- **PictureOfProffURL:** URL or path to the picture of proof.
- **IsApproved:** Boolean indicating whether the investment is approved.

### InvestmentApproval

- **InvestmentApprovalId (Primary Key):** Unique identifier for each investment approval.
- **InvestmentId (Foreign Key):** Reference to the associated investment.
- **ApproverID (Foreign Key):** Reference to the user who approved the investment.
- **IsApproved:** Boolean indicating whether the investment is approved.

### InvestorShare

- **InvestorShareId (Primary Key):** Unique identifier for each investor share.
- **CreatedAt:** Timestamp indicating when the investor share was created.
- **UpdatedAt:** Timestamp indicating when the investor share was last updated.
- **InvestorID (Foreign Key):** Reference to the investor user.
- **ShareValue:** Value of the share.
- **SharePercentage:** Percentage of the share.

### Salary

- **SalaryId (Primary Key):** Unique identifier for each salary.
- **EmployeeID (Foreign Key):** Reference to the employee user.
- **ReportingManager (Foreign Key):** Reference to the reporting manager user.
- **Designation:** Designation or job title.
- **Comment:** Comment related to the salary.
- **WorkDay:** Number of days worked.
- **SalaryAmount:** Amount of the salary.
- **IsApproved:** Boolean indicating whether the salary is approved.
- **IsPaid:** Boolean indicating whether the salary is paid.

### SalaryApproval

- **SalaryApprovalId (Primary Key):** Unique identifier for each salary approval.
- **SalaryId (Foreign Key):** Reference to the associated salary.
- **ApproverID (Foreign Key):** Reference to the user who approved the salary.
- **IsApproved:** Boolean indicating whether the salary is approved.

### InvestmentWithdraw

- **InvestmentWithdrawId (Primary Key):** Unique identifier for each investment withdrawal.
- **CreatedAt:** Timestamp indicating when the investment withdrawal was created.
- **InvestorID (Foreign Key):** Reference to the investor user.
- **InvestedAmount:** Amount of the investment withdrawal.
- **PictureOfProffURL:** URL or path to the picture of proof.
- **IsApproved:** Boolean indicating whether the investment withdrawal is approved.

### InvestmentWithdrawApproval

- **InvestmentWithdrawApprovalId (Primary Key):** Unique identifier for each investment withdrawal approval.
- **InvestmentWithdrawId (Foreign Key):** Reference to the associated investment withdrawal.
- **ApproverID (Foreign Key):** Reference to the user who approved the investment withdrawal.
- **IsApproved:** Boolean indicating whether the investment withdrawal is approved.

### ProfitShare

- **ProfitShareId (Primary Key):** Unique identifier for each profit share.
- **CreatedAt:** Timestamp indicating when the profit share was created.
- **Title:** Title of the profit share.
- **Description:** Description of the profit share.
- **ShareAmount:** Amount of the profit share.
- **SharePercentage:** Percentage of the profit share.
- **IsApproved:** Boolean indicating whether the profit share is approved.

### ProfitShareApproval

- **ProfitShareApprovalId (Primary Key):** Unique identifier for each profit share approval.
- **ProfitShareId (Foreign Key):** Reference to the associated profit share.
- **ApproverID (Foreign Key):** Reference to the user who approved the profit share.
- **IsApproved:** Boolean indicating whether the profit share is approved.

### ProfitShareReceived

- **ProfitShareReceivedId (Primary Key):** Unique identifier for each received profit share.
- **CreatedAt:** Timestamp indicating when the profit share was received.
- **Title:** Title of the received profit share.
- **ProfitShareId (Foreign Key):** Reference to the associated profit share.
- **ProfitShareReceiver (Foreign Key):** Reference to the user who received the profit share.
- **ShareAmount:** Amount of the received profit share.
- **SharePercentage:** Percentage of the received profit share.
- **IsPaid:** Boolean indicating whether the received profit share is paid.

---
```
Table ProductCategory {
  CategoryID int [pk]
  Title varchar
  CoverPicture varchar
  ProfilePicture varchar
}

Table ProductDescription {
  DescriptionID int [pk]
  CategoryID int [ref: > ProductCategory.CategoryID]
  DescriptionTitle varchar
  DescriptionText varchar
  SpecificationText varchar
}

Table ProductSizeChart {
  SizeChartID int [pk]
  CategoryID int [ref: > ProductCategory.CategoryID]
  SizeChart json
}

Table Product {
  ProductID int [pk]
  CategoryID int [ref: > ProductCategory.CategoryID]
  DescriptionID int [ref: > ProductDescription.DescriptionID]
  SizeChartID int [ref: > ProductSizeChart.SizeChartID]
  RealPrice decimal
  DiscountPercentage decimal
  SaleCount int
  visited int
  wishlisted int
  VideoURL varchar
  StoreId int [ref: > Store.StoreId]
}

Table ProductPhoto {
  PhotoID int [pk]
  ProductID int [ref: > Product.ProductID]
  PhotoURL varchar
}

Table Tag {
  TagID int [pk]
  TagName varchar
}

Table ProductTags {
  ProductTagID int [pk]
  ProductID int [ref: > Product.ProductID]
  TagID int [ref: > Tag.TagID]
}

Table ProductSizeQuantity {
  SizeQuantityID int [pk]
  ProductID int [ref: > Product.ProductID]
  ProductSize varchar
  QuantityInStock json
}

Table Review {
  ReviewID int [pk]
  ProductID int [ref: > Product.ProductID]
  Rating decimal
  Description varchar
}

Table Banner {
  BannerId int [pk]
  PhotoURL varchar
  BannerURL varchar
}

Table Offer {
  OfferId int [pk]
  OfferType varchar
  OfferTitle varchar
  OfferDescription varchar
  CoverPictureURL varchar
  RedirectURL varchar
  NotifyViaSMS bool
  NotifyViaApp bool
  NotificationFrequencyHour int
  SMSFrequencyHour int
  DurationDay int
  PromoCode varchar
  MinimumPurchase int
  DiscountPercentage int
  ProductList json
}

Table Notification {
  NotificationId int [pk]
  Title varchar
  Description varchar
  CoverPictureURL varchar
  RedirectURL varchar
  NotifyViaSMS bool
  NotifyViaApp bool
  NotificationFrequencyHour int
  SMSFrequencyHour int
  DurationDay int
  ProductList json
}

Table User {
  UserId int [pk]
  PhoneNo varchar
  FullName varchar
  Address varchar
  Email varchar
  City varchar
  Zone varchar
  Area varchar

  UserName varchar
  Parchase int
  Point int
  Visit int
  
  IsStaff bool
  StaffLevel varchar
  CreatedAt time
  UpdatedAt time
}

Table Store{
  StoreId int [pk]
  ContactName varchar
  ContactNumber varchar
  SecondContactNumber varchar
  StoreAddress varchar
  StoreCity varchar
  StoreZone varchar
  StoreArea varchar
}

Table Order {
  OrderID varchar [pk]
  CreatedAt time
  UpdatedAt time

  CustomerID int [ref: > User.UserId]
  CustomerName varchar
  CustomerPhone varchar
  CustomerEmail varchar
  
  CustomerAddress varchar
  CustomerCity varchar
  CustomerZone varchar
  CustomerArea varchar
  StoreId int [ref: > Store.StoreId]

  ProductValue double
  OrderValue double

  ItemType varchar
  ItemQuantity varchar
  ItemWeight double
  ItemDescription varchar
  
  DeliveryNote varchar
  DeliveryType varchar
  DeliveryCost double
  AmountToCollect varchar
  DeliveryConsignmentId varchar
  DeliveryTrackingURL varchar

  PaymentMethod varchar
  OrderStatus varchar
  PaymentStatus varchar

  Profit double
}

Table OrderedProduct{
  Id int [pk]
  OrderID int [ref: > Order.OrderID]
  ProductID int [ref: > Product.ProductID]
  ProductSize varchar
}

Table Purchase{
  PurchaseId int [pk]
  CreatedAt time
  Title varchar
  Description varchar
  PurchaseAmount int
  IsApproved bool
}

Table PurchaseApproval{
  PurchaseApprovalId int [pk]
  PurchaseId int [ref: > Purchase.PurchaseId]
  ApproverID int [ref: > User.UserId]
  IsApproved bool
}

Table PurchasePhoto {
  PhotoID int [pk]
  PurchaseId int [ref: > Purchase.PurchaseId]
  PhotoURL varchar
}

Table AccountBalance {
  AccountBalanceId int [pk]
  CreatedAt time
  InformerId int [ref: > User.UserId]
  CurrentBalance int 
  PictureOfProffURL varchar
  IsApproved bool
}

Table AccountBalanceApproval{
  AccountBalanceApprovalId int [pk]
  AccountBalanceId int [ref: > AccountBalance.AccountBalanceId]
  ApproverID int [ref: > User.UserId]
  IsApproved bool
}

Table Investment{
  InvestmentId int [pk]
  CreatedAt time
  InvestorID int [ref: > User.UserId]
  InvestedAmount int
  PictureOfProffURL varchar
  IsApproved bool
}

Table InvestmentApproval {
  InvestmentApprovalId int [pk]
  InvestmentId int [ref: > Investment.InvestmentId]
  ApproverID int [ref: > User.UserId]
  IsApproved bool
}

Table InvestorShare {
  InvestorShareId int [pk]
  CreatedAt time
  UpdatedAt time
  InvestorID int [ref: > User.UserId]
  ShareValue int
  SharePercentage double
}

Table Salary {
  SalaryId int [pk]
  EmployeeID int [ref: > User.UserId]
  ReportingManager int  [ref: > User.UserId]
  Designation varchar
  Comment varchar
  WorkDay int
  SalaryAmount int
  IsApproved bool
  IsPaid bool
}

Table SalaryApproval {
  SalaryApprovalId int [pk]
  SalaryId int [ref: > Salary.SalaryId]
  ApproverID int [ref: > User.UserId]
  IsApproved bool
}

Table InvestmentWithdraw {
  InvestmentWithdrawId int [pk]
  CreatedAt time
  InvestorID int [ref: > User.UserId]
  InvestedAmount int
  PictureOfProffURL varchar
  IsApproved bool
}

Table InvestmentWithdrawApproval {
  InvestmentWithdrawApprovalId int [pk]
  InvestmentWithdrawId int [ref: > InvestmentWithdraw.InvestmentWithdrawId]
  ApproverID int [ref: > User.UserId]
  IsApproved bool
}

Table ProfitShare {
  ProfitShareId int [pk]
  CreatedAt time
  Title varchar
  Description varchar
  ShareAmount int
  SharePercentage int
  IsApproved bool
}

Table ProfitShareApproval {
  ProfitShare int [pk]
  ProfitShareId int [ref: > ProfitShare.ProfitShareId]
  ApproverID int [ref: > User.UserId]
  IsApproved bool
}

Table ProfitShareRecived {
  ProfitShare int [pk]
  CreatedAt time
  Title verchar
  ProfitShareId int [ref: > ProfitShare.ProfitShareId]
  ProfitShareRiciver  int [ref: > User.UserId]
  ShareAmount int
  SharePercentage int
  IsPaid bool
}
```