Feature: Credit card number masking
    Credit and debit card numbers MUST be masked before they reach the
    gold layer.  Only the last 4 digits may be visible, formatted as
    XXXX-XXXX-XXXX-####.

    Scenario: Standard 16-digit card is masked
        Given a transaction with card number "1234567890123456"
        And a matching customer and franchise exist
        When the sales pipeline enriches the transaction
        Then the masked card number should be "XXXX-XXXX-XXXX-3456"

    Scenario: Masked card always starts with the fixed prefix
        Given a transaction with card number "9999888877776666"
        And a matching customer and franchise exist
        When the sales pipeline enriches the transaction
        Then the masked card number should start with "XXXX-XXXX-XXXX-"

    Scenario: Null card number produces null mask
        Given a transaction with a null card number
        And a matching customer and franchise exist
        When the sales pipeline enriches the transaction
        Then the masked card number should be null
