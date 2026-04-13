As a Senior QA Engineer, my approach to unit testing is to isolate each business logic component to ensure individual functions behave correctly under various conditions. To achieve >90% coverage, we will focus on path coverage, boundary value analysis, and error handling.

### 1. Module: Authentication Service
**Focus:** Login logic and state management for account locking.

| Test Case Description | Input | Expected Output |
| :--- | :--- | :--- |
| **Positive:** Successful login with valid credentials | Email: `user@test.com`, Pwd: `CorrectPass123` | Return `AuthToken`, Reset `fail_counter` to 0. |
| **Negative:** Invalid password - first attempt | Email: `user@test.com`, Pwd: `WrongPass` | Return `Unauthorized`, `fail_counter` incremented to 1. |
| **Boundary:** Third consecutive failed attempt | Email: `user@test.com`, Pwd: `WrongPass` | Return `Unauthorized`, `fail_counter` = 3. |
| **Edge:** Fourth attempt after account is locked | Email: `user@test.com`, Pwd: `CorrectPass123` | Return `AccountLockedError`, login denied even with correct password. |
| **Edge:** Case sensitivity and trimming | Email: ` USER@test.com `, Pwd: `CorrectPass123` | System trims whitespace/ignores case; returns `AuthToken`. |

---

### 2. Module: Product & Inventory Service
**Focus:** Filtering logic and real-time stock validation.

| Test Case Description | Input | Expected Output |
| :--- | :--- | :--- |
| **Positive:** Apply valid category filter | Category: `Electronics` | Return list of products where `category == 'Electronics'`. |
| **Negative:** Apply filter with no matching products | Category: `SpaceShips` | Return empty list `[]`. |
| **Boundary:** Check availability when stock is exactly 1 | ProductID: `P101`, Qty: `1` | Return `Available: True`. |
| **Boundary:** Check availability when stock is 0 | ProductID: `P102`, Qty: `1` | Return `Available: False`. |
| **Edge:** Check availability for negative quantity | ProductID: `P101`, Qty: `-5` | Throw `ValidationError` (Invalid Quantity). |

---

### 3. Module: Coupon Service
**Focus:** Date validation and string matching.

| Test Case Description | Input | Expected Output |
| :--- | :--- | :--- |
| **Positive:** Apply valid, active coupon | Code: `SAVE20`, Expiry: `2025-01-01` | Return `Discount: 20%`, `Status: Valid`. |
| **Negative:** Apply expired coupon | Code: `OLD50`, Expiry: `2020-01-01` | Return `Error: Coupon Expired`. |
| **Negative:** Apply non-existent code | Code: `FAKECODE` | Return `Error: Invalid Coupon`. |
| **Boundary:** Minimum order value for coupon | Order: `$49.99`, Coupon: `MIN50` | Return `Error: Minimum spend of $50 required`. |

---

### 4. Module: Cart Management
**Focus:** Integration between selection and stock state.

| Test Case Description | Input | Expected Output |
| :--- | :--- | :--- |
| **Positive:** Add available item to cart | ItemID: `123`, Stock: `5` | Item added; Cart total updated. |
| **Negative:** Add item that was sold out during session | ItemID: `456`, Stock: `0` | Return `Error: Item no longer available`. |
| **Boundary:** Add maximum allowable units of an item | ItemID: `789`, Stock: `10`, Qty: `10` | Item added; Stock check passes. |

---

### 5. Module: Payment Processing
**Focus:** Retry loop logic and terminal states.

| Test Case Description | Input | Expected Output |
| :--- | :--- | :--- |
| **Positive:** Payment succeeds on 1st attempt | Card: `Valid`, Status: `Success` | Return `Payment_Success`, Proceed to confirmation. |
| **Negative:** Payment fails on 1st attempt, succeeds on 2nd | Try 1: `Fail`, Try 2: `Success` | Log failure 1; Return `Payment_Success` on 2nd call. |
| **Boundary:** Payment fails 3 times (Max retries) | Try 1: `Fail`, Try 2: `Fail`, Try 3: `Fail` | Return `Order_Cancelled_Error`; Update order status to `Cancelled`. |
| **Edge:** Payment gateway timeout/network error | Gateway: `No Response` | Trigger retry logic as if payment failed. |

---

### 6. Module: Order Confirmation & Notification
**Focus:** Post-payment state and communication triggers.

| Test Case Description | Input | Expected Output |
| :--- | :--- | :--- |
| **Positive:** Generate Order ID after success | PaymentStatus: `Success` | Return unique `OrderID` (UUID/Hash). |
| **Positive:** Trigger email notification | OrderID: `ORD-001` | Call `EmailService.send()`, Return `Notification_Sent`. |
| **Negative:** Email service unavailable | OrderID: `ORD-001`, SMTP: `Down` | Log `EmailDeliveryFailure`; Return `OrderComplete` (Order still valid). |
| **Edge:** Confirming an order with an empty cart | Cart: `[]` | Throw `IllegalStateException` (Cannot confirm empty order). |

---

### Implementation Note for Coverage:
To ensure **>90% coverage**, during execution we must use a coverage tool (like `Istanbul/NYC` for JS, `JaCoCo` for Java, or `Coverage.py` for Python). We should specifically monitor **Branch Coverage** to ensure that both the `if (payment_failed)` and `else` paths are executed, as well as the `while` loop conditions for the login and payment retries.