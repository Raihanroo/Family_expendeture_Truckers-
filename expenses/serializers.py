from rest_framework import serializers

# DRF (Django REST Framework) থেকে serializers import করছি
# serializers হলো Database data কে JSON এ convert করার tool

from .models import FamilyMember, IncomeSource, ExpenseCategory, Expenditure, Expense

# আমাদের বানানো 4টা model import করছি


class IncomeSourceSerializer(serializers.ModelSerializer):
    # IncomeSource model এর জন্য serializer
    # যেমন: {"id": 1, "name": "চাকরি"} এই format এ data আসবে
    class Meta:
        model = IncomeSource  # কোন model এর জন্য
        fields = "__all__"  # সব field JSON এ আসবে


class ExpenseCategorySerializer(serializers.ModelSerializer):
    # MemberCategory model এর জন্য serializer
    # যেমন: {"id": 1, "name": "খাবার"} এই format এ data আসবে
    class Meta:
        model = ExpenseCategory  # কোন model এর জন্য
        fields = "__all__"  # সব field JSON এ আসবে


class FamilyMemberSerializer(serializers.ModelSerializer):
    # income_source is a CharField (not a ForeignKey), so we expose it directly.

    class Meta:
        model = FamilyMember
        fields = [
            "id",
            "user",
            "role",
            "joined_date",
            "name",
            "father_name",
            "mother_name",
            "phone_number",
            "address",
            "income_source",
            "salary",
        ]


class ExpenditureSerializer(serializers.ModelSerializer):
    # Expenditure model এর জন্য serializer

    member_name = serializers.CharField(
        source="member.name",
        read_only=True,
        # Member এর ID না, নাম দেখাবে (যেমন: "রাইহান")
    )
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
        # Category এর ID না, নাম দেখাবে (যেমন: "খাবার")
    )

    class Meta:
        model = Expenditure
        fields = [
            "id",  # Expenditure এর unique ID
            "member",  # Member এর ID
            "member_name",  # Member এর নাম (যেমন: "রাইহান")
            "category",  # Category এর ID
            "category_name",  # Category এর নাম (যেমন: "খাবার")
            "amount",  # কত টাকা খরচ হয়েছে
            "description",  # খরচের বিবরণ
            "date",  # কোন তারিখে খরচ হয়েছে
            "created_at",  # কখন record করা হয়েছে
        ]


class ExpenseSerializer(serializers.ModelSerializer):
    # Expense model এর জন্য serializer
    class Meta:
        model = Expense
        fields = "__all__"
