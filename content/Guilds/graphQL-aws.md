Title: REST API vs. GraphQL on AWS: A Simple Comparison Using API Gateway and AppSync
Date: 2025-06-01
Category: guide, Cloud Architecture
Tags: AWS, AppSync, GraphQL, REST, API Gateway, DynamoDB
Slug: rest-vs-graphql-api-aws
Author: Nima Moradi
Summary: A focused comparison of REST APIs using API Gateway and GraphQL using AppSync on AWS, illustrated with a simple shopping example involving Users, ShoppingCarts, and Items.

---

## Introduction

GraphQL is a query language for APIs that allows clients to request exactly the data they need in a single query. It eliminates the common inefficiencies of REST APIs, such as overfetching or underfetching, and provides a flexible, strongly typed interface that adapts well to evolving frontend requirements.


We’re not building a full e-commerce platform, but using a minimal online shopping example to highlight the differences in data access and structure. Think of a site similar to Amazon — which typically involves features like user accounts, shopping carts, item catalogs, dynamic offers, and price updates. In our simplified version, we’ll focus only on three core resources:

* User profile
* Shopping cart
* Items in the store

In REST, we would typically need to issue multiple requests to fetch these resources independently, or construct a custom aggregated endpoint (e.g. `/landingPageData`) that returns a composed payload. This kind of aggregation, however, introduces tight coupling between frontend versions and backend implementations. In real-world systems, this often leads to bloated response structures, versioning headaches, and reduced agility when iterating on UI features.

GraphQL addresses this differently: clients describe what data they need, and the server returns only that — in one structured response. This makes it easier to evolve APIs and match data needs exactly to UI use cases.

---

## The Example: Three Resources

Let’s assume a basic online shopping experience. We work with:

* `User`: profile data of a logged-in user.
* `ShoppingCart`: current items in the user's cart.
* `Item`: products available in the store.

These are three separate resources that must be fetched for the landing page. Depending on whether the user is logged in, the content changes — but in both REST and GraphQL, clients will want to *access a subset or all of them together*.

---

## Sample Data

Here are example items stored in DynamoDB tables:

**Product**

```json
{
  "productId": "prod007",
  "itemName": "External SSD 1TB",
  "price": 150,
  "quantityAvailable": 60
}
```

**User**

```json
{
  "userId": "uer4234",
  "authenticationCode": "242ashedpass",
  "familyName": "Moradi",
  "firstName": "Nima",
  "lastAccess": "2025-05-30T11:30:00Z",
  "username": "ni_moradi"
}
```

**Cart Item**

```json
{
  "userId": "uer4234",
  "productId": "prod004",
  "quantity": 2
}
```

---

## GraphQL Schema with AppSync

Below is a simplified GraphQL schema for our shopping scenario:

```graphql
type CartItem {
  productId: String!
  quantity: Int!
  product: Product
}

type Product {
  productId: ID!
  itemName: String!
  quantityAvailable: Int!
  price: Float!
}

type ShoppingCart {
  userId: ID!
  items: [CartItem!]!
}

type User {
  userId: ID!
  username: String!
  familyName: String
  firstName: String
  authenticationCode: String!
  lastAccess: AWSDateTime
  shoppingCart: ShoppingCart
}

type Mutation {
  updateProductQuantity(productId: ID!, quantityAvailable: Int!): Product
  addItemToCart(userId: ID!, productId: ID!, quantity: Int!): CartItem
  removeItemFromCart(userId: ID!, productId: ID!): CartItem
  updateCartItemQuantity(userId: ID!, productId: ID!, quantity: Int!): CartItem
}

type Query {
  getUser(userId: ID!): User
  listUsers: [User]
  getProduct(productId: ID!): Product
  listProducts: [Product]
  getShoppingCart(userId: ID!): ShoppingCart
}
```

Notice that `CartItem` contains a `product` field, allowing nested access to product details for each cart entry.

---

## ShoppingCart Resolver (VTL)

Here is a simple VTL template for resolving a query to fetch a user's shopping cart from DynamoDB:

```json
{
  "version": "2018-05-29",
  "operation": "Query",
  "query": {
    "expression": "userId = :userId",
    "expressionValues": {
      ":userId": $util.dynamodb.toDynamoDBJson($ctx.args.userId)
    }
  }
}
```

---

## Sample GraphQL Query and Response

Query:

```graphql
query GetCart {
  getShoppingCart(userId: "uer4234") {
    items {
      productId
      quantity
      product {
        productId
        itemName
        price
        quantityAvailable
      }
    }
  }
}
```

Response:

```json
{
  "data": {
    "getShoppingCart": {
      "items": [
        {
          "productId": "prod002",
          "quantity": 1,
          "product": {
            "itemName": "Mechanical Keyboard",
            "price": 99.99,
            "productId": "prod002",
            "quantityAvailable": 150
          }
        },
        {
          "productId": "prod003",
          "quantity": 1,
          "product": {
            "itemName": "Wireless Mouse",
            "price": 25,
            "productId": "prod003",
            "quantityAvailable": 200
          }
        },
        {
          "productId": "prod009",
          "quantity": 1,
          "product": {
            "itemName": "Smartwatch",
            "price": 250,
            "productId": "prod009",
            "quantityAvailable": 40
          }
        }
      ]
    }
  }
}
```

This example demonstrates how GraphQL enables nested access and aggregation of related data without requiring multiple round-trips or additional client-side composition logic.
