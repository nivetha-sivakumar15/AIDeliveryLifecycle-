# Technical Design Document: E-Commerce Authentication & Order Fulfillment System

## 1. System Overview
This system provides a secure end-to-end e-commerce experience, encompassing user authentication, product discovery, inventory-aware shopping cart management, coupon-based checkout, and a resilient payment processing pipeline. The primary objective is to ensure security (account locking), data integrity (stock validation), and reliability (payment retries).

## 2. Architecture Design
The system follows a **Microservices Architecture** to decouple concerns and ensure scalability across different domains:

*   **Identity Service:** Manages user credentials and security state (account locking).
*   **Catalog Service:** Handles product data, filtering logic, and inventory levels.
*   **Cart Service:** Manages transient state of user selections and coordinates stock checks.
*   **Order & Promotion Service:** Orchestrates the checkout process and validates discount logic.
*   **Payment Service:** Interfaces with credit card processors and manages transaction state and retries.
*   **Notification Service:** Asynchronous service for triggering email confirmations.

## 3. Component Breakdown

### 3.1 Identity Provider
*   **Function:** Validates `email` and `password`.
*   **Logic:** Maintains a `failed_login_attempts` counter. Triggers an `account_locked` state once the threshold (>3) is met.

### 3.2 Product Catalog & Inventory
*   **Function:** Serves filtered product lists.
*   **Logic:** Performs a real-time `stock_check` before confirming an "Add to Cart" action.

### 3.3 Checkout Engine
*   **Function:** Applies business rules to coupons.
*   **Logic:** Validates `coupon_code` against `expiry_date` and `usage_status`.

### 3.4 Payment Gateway Wrapper
*   **Function:** Handles Credit Card transactions.
*   **Logic:** Implements a retry loop (Max Retries: 2). On the 3rd total failure, it signals the Order Service to trigger `order_cancelled`.

## 4. Data Flow
1.  **Auth Flow:** User inputs credentials -> System checks against DB -> On success, session starts. On failure, increment counter -> If counter > 3, update status to `Locked`.
2.  **Browsing Flow:** User applies filters -> Catalog Service returns filtered list.
3.  **Cart Flow:** User selects item -> System queries Inventory -> If `available`, add to cart; else, return error.
4.  **Checkout Flow:** User enters coupon -> System validates status/expiry -> Update order total.
5.  **Payment Flow:** Submit CC details -> If fail, retry up to 2 times -> On terminal failure, cancel order. On success, move to confirmation.
6.  **Notification Flow:** Success signal triggers Email template generation and dispatch.

## 5. API Design

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/v1/auth/login` | POST | Authenticates user; manages failure counts and locking. |
| `/v1/products` | GET | Returns products based on filter parameters. |
| `/v1/cart/add` | POST | Validates availability and adds item to session cart. |
| `/v1/coupons/validate` | POST | Checks if a coupon is valid and returns discount value. |
| `/v1/payments/process` | POST | Executes CC transaction with built-in retry logic. |
| `/v1/orders/confirm` | GET | Generates final receipt and triggers email. |

## 6. Database Design (Conceptual)

### Table: Users
*   `user_id` (PK)
*   `email` (Unique)
*   `password_hash`
*   `login_attempts` (Int)
*   `is_locked` (Boolean)

### Table: Products
*   `product_id` (PK)
*   `name`
*   `stock_quantity` (Int)
*   `filters` (JSON/Metadata)

### Table: Coupons
*   `coupon_code` (PK)
*   `discount_type`
*   `expiry_date` (Timestamp)
*   `is_active` (Boolean)

### Table: Orders
*   `order_id` (PK)
*   `user_id` (FK)
*   `status` (Pending, Success, Cancelled)
*   `payment_attempts` (Int)

## 7. Error Handling & Edge Cases

| Scenario | System Response |
| :--- | :--- |
| **Login Failure > 3** | Set `is_locked = true`; Deny all subsequent login attempts for that email. |
| **Out of Stock** | Block "Add to Cart" action; Return "Item Unavailable" message. |
| **Expired/Invalid Coupon** | Return "Invalid or Expired Coupon" error; Retain original order total. |
| **Payment Failure (1st & 2nd)** | Prompt user for retry; Do not cancel order. |
| **Payment Failure (3rd)** | Set Order Status to `Cancelled`; Stop retry attempts. |

## 8. Assumptions
*   The system uses a persistent data store to track login attempts across sessions.
*   "Credit Card" is the primary payment method mentioned; others are not in scope.
*   Availability check occurs at the moment of adding to cart to prevent downstream checkout failures.
*   The email notification is triggered only after the Payment Service confirms a successful transaction.