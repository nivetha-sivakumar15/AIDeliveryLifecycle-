As the QA Lead, I have outlined the following end-to-end (E2E) test scenarios. These cover the critical business paths, including security constraints, inventory logic, and payment recovery flows, ensuring over 70% of the business logic is validated.

### 1. Happy Path: Successful End-to-End Purchase
*   **Scenario Name:** E2E_01_Standard_User_Purchase_Flow
*   **Steps:**
    1.  Navigate to the login page and enter valid email/password.
    2.  Browse products and apply a specific category filter.
    3.  Select a product that is "In Stock" and add it to the cart.
    4.  Navigate to the checkout page.
    5.  Enter a valid, active discount coupon.
    6.  Enter valid credit card details and submit payment.
*   **Expected Outcome:** 
    *   Login is successful.
    *   Cart reflects the correct item and stock is validated.
    *   Coupon discount is applied to the total price.
    *   Order confirmation page is displayed and a confirmation email is received.

### 2. Failure Path: Account Lockout Security
*   **Scenario Name:** E2E_02_Security_Account_Lockout_Mechanism
*   **Steps:**
    1.  Navigate to the login page.
    2.  Enter valid email but incorrect password 3 times consecutively.
    3.  Attempt a 4th login with the correct password.
*   **Expected Outcome:** 
    *   After the 3rd failed attempt, the system displays an "Account Locked" message.
    *   The 4th attempt (even with correct credentials) is rejected due to the lock status.

### 3. Edge Case: Inventory Depletion during Browsing
*   **Scenario Name:** E2E_03_Stock_Availability_Validation
*   **Steps:**
    1.  Login to the system.
    2.  Search for a product that has only 1 unit remaining in stock.
    3.  In a separate administrative session (or background process), reduce that item's stock to 0.
    4.  Attempt to add the item to the cart from the user session.
*   **Expected Outcome:** 
    *   System performs a real-time availability check.
    *   An error message appears stating the item is no longer available.
    *   The item is not added to the cart.

### 4. Failure Path: Invalid Coupon Application
*   **Scenario Name:** E2E_04_Coupon_Validation_Rules
*   **Steps:**
    1.  Login and add items to the cart.
    2.  Navigate to the checkout/payment screen.
    3.  Apply an expired coupon code.
    4.  Apply a non-existent/gibberish coupon code.
*   **Expected Outcome:** 
    *   System displays a clear error message: "Coupon is invalid or expired."
    *   The order total remains unchanged.
    *   User is allowed to proceed to payment without the discount.

### 5. Recovery Path: Payment Retry Logic (Success on 2nd Attempt)
*   **Scenario Name:** E2E_05_Payment_Processing_Retry_Success
*   **Steps:**
    1.  Proceed to payment with a full cart.
    2.  Enter credit card details that trigger a "Declined" response from the gateway.
    3.  Observe the retry prompt.
    4.  Enter valid credit card details on the second attempt.
*   **Expected Outcome:** 
    *   System identifies the first failure and allows a retry.
    *   Upon the second (successful) attempt, the order is processed.
    *   Order confirmation is generated.

### 6. Failure Path: Order Cancellation (Max Payment Retries Exceeded)
*   **Scenario Name:** E2E_06_Payment_Processing_Max_Retry_Failure
*   **Steps:**
    1.  Proceed to payment with a full cart.
    2.  Fail the payment attempt 1 time.
    3.  Fail the payment attempt a 2nd time (Retry 1).
    4.  Fail the payment attempt a 3rd time (Retry 2).
*   **Expected Outcome:** 
    *   After the final failure (3 total attempts), the system stops the retry loop.
    *   The order is automatically transitioned to "Cancelled" status.
    *   The user is notified that the order could not be processed and the cart is either saved or emptied based on business requirements.

### 7. Edge Case: Filter Integrity and Search Accuracy
*   **Scenario Name:** E2E_07_Product_Browsing_Data_Integrity
*   **Steps:**
    1.  Login and navigate to the product catalog.
    2.  Apply multiple filters (e.g., Price Range: $10-$50 AND Category: Electronics).
    3.  Verify the displayed results against the filter criteria.
    4.  Add the filtered item to the cart.
*   **Expected Outcome:** 
    *   Only products matching ALL active filters are displayed.
    *   "Availability check" confirms the filtered items are eligible for purchase.