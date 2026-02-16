"""Behavior tests for card masking — backed by card_masking.feature."""

from pytest_bdd import given, parsers, scenario, then, when

from src.transformations import enrich_bakehouse_sales
from tests.schemas import TRANSACTION_SCHEMA


pytest_plugins = [
    "tests.behavior_tests.card_masking_data",
]

FEATURE = "scenarios/card_masking.feature"


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------
@scenario(FEATURE, "Standard 16-digit card is masked")
def test_standard_card_masked(): ...


@scenario(FEATURE, "Masked card always starts with the fixed prefix")
def test_mask_prefix(): ...


@scenario(FEATURE, "Null card number produces null mask")
def test_null_card(): ...


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------
@given(
    parsers.parse('a transaction with card number "{card_number}"'),
    target_fixture="transaction",
)
def given_transaction_with_card(spark, card_number, single_customer, single_franchise):
    from datetime import datetime
    from decimal import Decimal

    data = [
        (
            1,
            datetime(2024, 1, 1, 12, 0),
            1,
            10,
            "Bread",
            1,
            Decimal("2.00"),
            Decimal("2.00"),
            "Credit Card",
            Decimal(card_number),
        ),
    ]
    return spark.createDataFrame(data, TRANSACTION_SCHEMA)


@given("a transaction with a null card number", target_fixture="transaction")
def given_transaction_null_card(spark):
    from datetime import datetime
    from decimal import Decimal

    data = [
        (
            1,
            datetime(2024, 1, 1, 12, 0),
            1,
            10,
            "Bread",
            1,
            Decimal("2.00"),
            Decimal("2.00"),
            "Cash",
            None,
        ),
    ]
    return spark.createDataFrame(data, TRANSACTION_SCHEMA)


@given("a matching customer and franchise exist")
def given_matching_dimensions():
    # single_customer and single_franchise fixtures are already injected
    ...


@when(
    "the sales pipeline enriches the transaction",
    target_fixture="enriched_result",
)
def when_enrich(transaction, single_customer, single_franchise):
    return enrich_bakehouse_sales(transaction, single_customer, single_franchise)


@then(parsers.parse('the masked card number should be "{expected}"'))
def then_masked_equals(enriched_result, expected):
    masked = enriched_result.collect()[0]["masked_cardNumber"]
    assert masked == expected


@then(parsers.parse('the masked card number should start with "{prefix}"'))
def then_masked_starts_with(enriched_result, prefix):
    masked = enriched_result.collect()[0]["masked_cardNumber"]
    assert masked.startswith(prefix)


@then("the masked card number should be null")
def then_masked_is_null(enriched_result):
    masked = enriched_result.collect()[0]["masked_cardNumber"]
    assert masked is None
