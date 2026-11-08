
import sqlite3
from datetime import date
import calendar

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ==========================================
# ExpenseEase - Personal Expense Tracker
# ==========================================

st.set_page_config(
    page_title="ExpenseEase",
    page_icon="💜",
    layout="wide"
)

DB_NAME = "expenses.db"

CATEGORIES = [
    "Food", "Travel", "Shopping", "Bills", "Education",
    "Health", "Entertainment", "Others"
]

# ==========================================
# STYLING
# ==========================================

st.markdown("""
<style>

:root {
    --ink: #241334;
    --purple: #59258b;
    --purple-dark: #3d1765;
    --lavender: #f1e8fb;
    --border: #d8c4eb;
}

.stApp {
    background: linear-gradient(
        135deg,
        #fbf8ff 0%,
        #f3eaff 55%,
        #fffaff 100%
    );
    color: var(--ink);
}

/* HEADINGS */

h1 {
    color: #491477 !important;
    font-weight: 800 !important;
}

h2, h3, h4 {
    color: #68299b !important;
    font-weight: 750 !important;
}

/* NORMAL TEXT */

p, li, label,
[data-testid="stMarkdownContainer"] p {
    color: #321747 !important;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #e9d8fa 0%,
        #d9bff2 100%
    );
    border-right: 1px solid #d8c4eb;
}

[data-testid="stSidebar"] * {
    color: #32104e !important;
}

/* SUCCESS MESSAGE */

[data-testid="stAlert"]:has([data-testid="stSuccessIcon"]) {
    background-color: #d9fbe5 !important;
    border: 2px solid #28a45b !important;
    border-radius: 12px;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span {
    font-weight: 750 !important;
}

/* ERROR MESSAGE */

[data-testid="stAlert"]:has([data-testid="stErrorIcon"]) {
    background-color: #ffe1e1 !important;
    border: 2px solid #e05252 !important;
}

[data-testid="stAlert"]:has([data-testid="stErrorIcon"]) p {
    color: #991b1b !important;
}

/* WARNING MESSAGE */

[data-testid="stAlert"]:has([data-testid="stWarningIcon"]) {
    background-color: #fff0c2 !important;
    border: 2px solid #d69b16 !important;
}

[data-testid="stAlert"]:has([data-testid="stWarningIcon"]) p {
    color: #805000 !important;
}

/* INFO MESSAGE */

[data-testid="stAlert"]:has([data-testid="stInfoIcon"]) {
    background-color: #e0efff !important;
    border: 2px solid #4385c7 !important;
}

[data-testid="stAlert"]:has([data-testid="stInfoIcon"]) p {
    color: #174c80 !important;
}

/* INPUT FIELDS */

input, textarea {
    background-color: #ffffff !important;
    color: #241334 !important;
    border: 1px solid #a77bc8 !important;
}

input::placeholder,
textarea::placeholder {
    color: #766783 !important;
    opacity: 1;
}

/* DROPDOWN SELECTED VALUE */

[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid #a77bc8 !important;
    color: #35134f !important;
}

/* DROPDOWN MENU */

[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
    background-color: #ffffff !important;
}

/* CATEGORY OPTIONS */

[role="option"] {
    background-color: #ffffff !important;
    color: #321747 !important;
    font-weight: 600 !important;
}

[role="option"]:hover {
    background-color: #ead8fa !important;
    color: #481276 !important;
}

[aria-selected="true"] {
    background-color: #e3cef6 !important;
    color: #42116c !important;
    font-weight: 800 !important;
}

/* BUTTONS */

div.stButton > button,
div.stDownloadButton > button,
.stFormSubmitButton > button {

    background: linear-gradient(
        90deg,
        #6b32a0,
        #884fc0
    );

    color: #ffffff !important;
    border: 0;
    border-radius: 11px;
    font-weight: 700;
    min-height: 2.7rem;

    box-shadow: 0 3px 10px rgba(75, 35, 110, .15);
}

div.stButton > button:hover,
div.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #42186d !important;
    color: #ffffff !important;
}

/* METRICS */

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #dfcbed;
    border-radius: 16px;
    padding: 18px 18px 14px;
    box-shadow: 0 5px 18px rgba(75, 35, 110, .08);
}

[data-testid="stMetricLabel"] {
    color: #624477 !important;
    font-weight: 650;
}

[data-testid="stMetricValue"] {
    color: #40156a !important;
    font-weight: 800 !important;
}

/* DATA TABLE */

[data-testid="stDataFrame"] {
    background: #ffffff;
    border: 1px solid #e0d0ed;
    border-radius: 12px;
    padding: 5px;
}

/* CAPTIONS */

[data-testid="stCaptionContainer"] {
    color: #59466b !important;
}

/* HORIZONTAL LINE */

hr {
    border-color: #ddcbea;
}


/* DELETE CONFIRMATION MESSAGE */
[data-testid="stAlert"]:has([data-testid="stWarningIcon"]) p {
    color: #713f12 !important;
    font-size: 16px !important;
    font-weight: 800 !important;
}

/* DELETE BUTTON */
div.stButton > button {
    color: #ffffff !important;
}

/* DELETE CONFIRMATION BUTTONS */
button[kind="secondary"] {
    color: #ffffff !important;
}

/* DELETE TEXT AND LABELS */
[data-testid="stMarkdownContainer"] strong {
    color: #321047 !important;
}

/* FORCE TEXT VISIBILITY - SMART RECOMMENDATIONS */

.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp div,
.stApp li {
    color: #24123d !important;
}

/* Headings */
.stApp h1,
.stApp h2,
.stApp h3 {
    color: #4c1d75 !important;
    font-weight: 800 !important;
}

/* Info messages */
[data-testid="stAlert"] {
    background-color: #eee5ff !important;
    border: 2px solid #8b5cf6 !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span {
    color: #24123d !important;
    opacity: 1 !important;
}

/* Success messages */
[data-testid="stAlert"][kind="success"] {
    background-color: #dcfce7 !important;
}

/* Warning messages */
[data-testid="stAlert"][kind="warning"] {
    background-color: #fef3c7 !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background-color: #f3e8ff !important;
    padding: 12px !important;
    border-radius: 10px !important;
}

[data-testid="stMetric"] * {
    color: #24123d !important;
    opacity: 1 !important;
}

/* Charts and labels */
.stMarkdown, .stMarkdown p {
    color: #24123d !important;
}

# ==========================================
# DATABASE
# ==========================================

def get_connection():
    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )


def initialize_database():

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_name TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT
            )
        """)

        conn.commit()

# NEW SAVINGS GOALS FUNCTION
def initialize_savings_goals():

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                saved_amount REAL DEFAULT 0,
                target_date TEXT
            )
        """)

        conn.commit()       


def load_expenses():

    with get_connection() as conn:

        df = pd.read_sql_query(
            """
            SELECT id, expense_name, amount,
                   category, date, description
            FROM expenses
            ORDER BY date DESC, id DESC
            """,
            conn
        )

    if not df.empty:

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        ).fillna(0)

    return df


def money(value):
    return f"₹{float(value):,.2f}"


initialize_database()
initialize_savings_goals()
df = load_expenses()


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("💜 ExpenseEase")
st.sidebar.caption("Personal Expense Tracker")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Add Expense",
        "Transactions",
        "Monthly Summary",
        "Yearly Summary",
        "Smart Recommendations",
        "Savings Goals",
        "Expense Prediction",
        "Financial Health Score"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Track better. Spend smarter.")

# ==========================================
# SUCCESS MESSAGE
# ==========================================

if st.session_state.get("expenseease_flash"):

    flash_message = st.session_state.pop("expenseease_flash")

    st.markdown(
        f"""
        <div style="
            background-color: #d1fae5;
            color: #065f46;
            padding: 16px;
            border-radius: 12px;
            border: 2px solid #10b981;
            font-size: 17px;
            font-weight: 800;
            margin-bottom: 15px;
        ">
            ✅ {flash_message}
        </div>
        """,
        unsafe_allow_html=True
    )
# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.title("💜 ExpenseEase Dashboard")

    st.write("Your spending overview at a glance.")

    today = date.today()

    month_df = df[
        (df["date"].dt.month == today.month) &
        (df["date"].dt.year == today.year)
    ] if not df.empty else df

    total_spent = df["amount"].sum() if not df.empty else 0

    monthly_spent = (
        month_df["amount"].sum()
        if not month_df.empty else 0
    )

    transaction_count = len(df)

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Expenses", money(total_spent))
    c2.metric("This Month", money(monthly_spent))
    c3.metric("Transactions", transaction_count)

    st.subheader("Recent Transactions")

    if df.empty:

        st.info(
            "No expenses yet. Go to Add Expense to record your first expense."
        )

    else:

        recent = df.head(8).copy()

        recent["date"] = recent["date"].dt.strftime("%d-%m-%Y")
        recent["amount"] = recent["amount"].map(money)

        st.dataframe(
            recent[
                [
                    "expense_name",
                    "amount",
                    "category",
                    "date",
                    "description"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Spending by Category")

        category_data = (
            df.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots()

        category_data.plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax,
            ylabel=""
        )

        st.pyplot(fig)
        plt.close(fig)


# ==========================================
# ADD EXPENSE
# ==========================================

elif page == "Add Expense":

    st.title("➕ Add a New Expense")

    with st.form(
        "add_expense_form",
        clear_on_submit=True
    ):

        expense_name = st.text_input(
            "Expense name",
            placeholder="e.g. Lunch"
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=10.0,
            format="%.2f"
        )

        category = st.selectbox(
            "Category",
            CATEGORIES
        )

        expense_date = st.date_input(
            "Date",
            value=date.today()
        )

        description = st.text_area(
            "Description (optional)"
        )

        submitted = st.form_submit_button(
            "Add Expense"
        )

        if submitted:

            if not expense_name.strip():

                st.error("Please enter an expense name.")

            elif amount <= 0:

                st.error(
                    "Please enter an amount greater than zero."
                )

            else:

                with get_connection() as conn:

                    conn.execute(
                        """
                        INSERT INTO expenses
                        (expense_name, amount, category, date, description)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            expense_name.strip(),
                            float(amount),
                            category,
                            expense_date.isoformat(),
                            description.strip()
                        )
                    )

                    conn.commit()

                st.session_state["expenseease_flash"] = (
                    "🎉 Expense added successfully!"
                )

                st.rerun()


# ==========================================
# TRANSACTIONS
# ==========================================

elif page == "Transactions":

    st.title("📋 Transactions")

    if df.empty:

        st.info("No transactions available yet.")

    else:

        search_text = st.text_input(
            "Search by expense name"
        )

        categories = [
            "All"
        ] + sorted(
            df["category"].dropna().unique().tolist()
        )

        selected_category = st.selectbox(
            "Filter by category",
            categories
        )

        filtered = df.copy()

        if search_text:

            filtered = filtered[
                filtered["expense_name"].str.contains(
                    search_text,
                    case=False,
                    na=False
                )
            ]

        if selected_category != "All":

            filtered = filtered[
                filtered["category"] == selected_category
            ]

        display_df = filtered.copy()

        display_df["date"] = (
            display_df["date"].dt.strftime("%d-%m-%Y")
        )

        display_df["amount"] = display_df["amount"].map(money)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = filtered.copy()

        csv_data["date"] = (
            csv_data["date"].dt.strftime("%Y-%m-%d")
        )

        st.download_button(
            "📥 Download Transactions CSV",
            data=csv_data.to_csv(index=False).encode("utf-8"),
            file_name="ExpenseEase_Transactions.csv",
            mime="text/csv"
        )

        st.subheader("Edit or Delete an Expense")

        expense_ids = filtered["id"].tolist()

        if expense_ids:

            selected_id = st.selectbox(
                "Select transaction ID",
                expense_ids
            )

            selected_row = df[
                df["id"] == selected_id
            ].iloc[0]

            with st.form("edit_expense_form"):

                new_name = st.text_input(
                    "Expense name",
                    value=selected_row["expense_name"]
                )

                new_amount = st.number_input(
                    "Amount (₹)",
                    min_value=0.0,
                    value=float(selected_row["amount"]),
                    step=10.0
                )

                current_category = selected_row["category"]

                category_index = (
                    CATEGORIES.index(current_category)
                    if current_category in CATEGORIES
                    else 0
                )

                new_category = st.selectbox(
                    "Category",
                    CATEGORIES,
                    index=category_index
                )

                new_date = st.date_input(
                    "Date",
                    value=selected_row["date"].date()
                )

                old_description = selected_row["description"]

                new_description = st.text_area(
                    "Description",
                    value=(
                        ""
                        if pd.isna(old_description)
                        else str(old_description)
                    )
                )

                save_edit = st.form_submit_button(
                    "Save Changes"
                )

                if save_edit:

                    if not new_name.strip() or new_amount <= 0:

                        st.error(
                            "Enter a valid name and amount."
                        )

                    else:

                        with get_connection() as conn:

                            conn.execute(
                                """
                                UPDATE expenses
                                SET expense_name=?,
                                    amount=?,
                                    category=?,
                                    date=?,
                                    description=?
                                WHERE id=?
                                """,
                                (
                                    new_name.strip(),
                                    float(new_amount),
                                    new_category,
                                    new_date.isoformat(),
                                    new_description.strip(),
                                    int(selected_id)
                                )
                            )

                            conn.commit()

                        st.session_state["expenseease_flash"] = (
                            "✏️ Expense updated successfully!"
                        )

                        st.rerun()

            if st.button("🗑️ Delete Selected Expense"):

                st.session_state["confirm_delete_id"] = int(
                    selected_id
                )

            if st.session_state.get(
                "confirm_delete_id"
            ) == int(selected_id):

                st.markdown("""
<div style="
    background-color: #ffe0e0;
    color: #991b1b;
    padding: 15px;
    border: 2px solid #dc2626;
    border-radius: 10px;
    font-size: 17px;
    font-weight: 800;
">
    ⚠️ Are you sure you want to delete this expense?
</div>
""", unsafe_allow_html=True)

                yes_col, no_col = st.columns(2)

                if yes_col.button("Yes, delete"):

                    with get_connection() as conn:

                        conn.execute(
                            "DELETE FROM expenses WHERE id=?",
                            (int(selected_id),)
                        )

                        conn.commit()

                    st.session_state.pop(
                        "confirm_delete_id",
                        None
                    )

                    st.session_state["expenseease_flash"] = (
                        "🗑️ Expense deleted successfully!"
                    )

                    st.rerun()

                if no_col.button("Cancel"):

                    st.session_state.pop(
                        "confirm_delete_id",
                        None
                    )

                    st.rerun()


# ==========================================
# MONTHLY SUMMARY
# ==========================================

elif page == "Monthly Summary":

    st.title("📅 Monthly Summary")

    if df.empty:

        st.info(
            "Add expenses to view your monthly summary."
        )

    else:

        available_months = sorted(
            df["date"].dropna().dt.to_period("M").unique(),
            reverse=True
        )

        month_options = [
            str(item) for item in available_months
        ]

        selected_month = st.selectbox(
            "Choose month",
            month_options
        )

        year_num, month_num = map(
            int,
            selected_month.split("-")
        )

        monthly_data = df[
            (df["date"].dt.year == year_num) &
            (df["date"].dt.month == month_num)
        ].copy()

        monthly_total = monthly_data["amount"].sum()

        transaction_total = len(monthly_data)

        daily_average = (
            monthly_total /
            calendar.monthrange(year_num, month_num)[1]
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Spent",
            money(monthly_total)
        )

        col2.metric(
            "Transactions",
            transaction_total
        )

        col3.metric(
            "Average per Calendar Day",
            money(daily_average)
        )

        # BUDGET COMPARISON

        st.subheader("Budget vs Actual Comparison")

        budget_key = f"budget_{selected_month}"

        monthly_budget = st.number_input(
            "Set monthly budget (₹)",
            min_value=0.0,
            value=float(
                st.session_state.get(
                    budget_key,
                    10000.0
                )
            ),
            step=500.0,
            key=f"budget_input_{selected_month}"
        )

        st.session_state[budget_key] = monthly_budget

        if monthly_budget > 0:

            remaining = monthly_budget - monthly_total

            b1, b2 = st.columns(2)

            b1.metric(
                "Budget",
                money(monthly_budget)
            )

            b2.metric(
                "Remaining" if remaining >= 0 else "Over Budget",
                money(abs(remaining))
            )

            st.progress(
                min(monthly_total / monthly_budget, 1.0)
            )

            if remaining >= 0:

                st.success(
                    f"You are within budget by {money(remaining)}."
                )

            else:

                st.warning(
                    f"You have exceeded your budget by {money(abs(remaining))}."
                )

        else:

            st.info(
                "Enter a budget greater than zero to compare spending."
            )

        # MONTHLY TREND

        st.subheader("Monthly Spending Trend")

        trend = df.copy()

        trend["month"] = (
            trend["date"].dt.to_period("M").astype(str)
        )

        trend_data = (
            trend.groupby("month")["amount"]
            .sum()
            .sort_index()
        )

        fig, ax = plt.subplots()

        trend_data.plot(
            kind="line",
            marker="o",
            ax=ax
        )

        ax.set_xlabel("Month")
        ax.set_ylabel("Amount (₹)")
        ax.tick_params(axis="x", rotation=45)

        st.pyplot(fig)
        plt.close(fig)

        # CATEGORY AND DAILY SPENDING

        left, right = st.columns(2)

        with left:

            st.subheader("Category Breakdown")

            category_data = (
                monthly_data.groupby("category")["amount"].sum()
            )

            if not category_data.empty:

                fig, ax = plt.subplots()

                category_data.plot(
                    kind="pie",
                    autopct="%1.1f%%",
                    ax=ax,
                    ylabel=""
                )

                st.pyplot(fig)
                plt.close(fig)

            else:

                st.info("No category data for this month.")

        with right:

            st.subheader("Daily Spending")

            daily_data = (
                monthly_data.groupby(
                    monthly_data["date"].dt.day
                )["amount"].sum()
            )

            if not daily_data.empty:

                fig, ax = plt.subplots()

                daily_data.plot(
                    kind="bar",
                    ax=ax
                )

                ax.set_xlabel("Day of month")
                ax.set_ylabel("Amount (₹)")

                st.pyplot(fig)
                plt.close(fig)

            else:

                st.info("No daily spending data.")

        # MONTHLY REPORT

        st.subheader("Monthly Expense Report")

        report = monthly_data.copy()

        report["date"] = (
            report["date"].dt.strftime("%Y-%m-%d")
        )

        st.download_button(
            "📥 Download Monthly Report",
            data=report.to_csv(index=False).encode("utf-8"),
            file_name=f"ExpenseEase_{selected_month}_Report.csv",
            mime="text/csv"
        )

        # SPENDING INSIGHTS

        st.subheader("Spending Insights")

        if not monthly_data.empty:

            highest_category = (
                monthly_data.groupby("category")["amount"]
                .sum()
                .idxmax()
            )

            highest_category_amount = (
                monthly_data.groupby("category")["amount"]
                .sum()
                .max()
            )

            largest_expense = monthly_data.loc[
                monthly_data["amount"].idxmax()
            ]

            st.write(
                f"- Highest spending category: **{highest_category}** "
                f"({money(highest_category_amount)})"
            )

            st.write(
                f"- Largest individual expense: "
                f"**{largest_expense['expense_name']}** "
                f"({money(largest_expense['amount'])})"
            )

            st.write(
                f"- Average expense transaction: "
                f"{money(monthly_total / len(monthly_data))}"
            )


# ==========================================
# YEARLY SUMMARY
# ==========================================

elif page == "Yearly Summary":

    st.title("🗓️ Yearly Summary")

    if df.empty:

        st.info("Add expenses to view your yearly summary.")

    else:

        available_years = sorted(
            df["date"].dropna().dt.year.unique().tolist(),
            reverse=True
        )

        if not available_years:
            st.info("No valid expense dates available.")

        else:

            selected_year = st.selectbox(
                "Choose year",
                available_years
            )

            yearly_data = df[
                df["date"].dt.year == int(selected_year)
            ].copy()

            yearly_total = yearly_data["amount"].sum()
            yearly_transactions = len(yearly_data)
            monthly_average = yearly_total / 12

            col1, col2, col3 = st.columns(3)

            col1.metric("Yearly Total", money(yearly_total))
            col2.metric("Transactions", yearly_transactions)
            col3.metric("Monthly Average", money(monthly_average))

            # MONTHLY SPENDING

            st.subheader("Monthly Spending")

            yearly_data["month_number"] = (
                yearly_data["date"].dt.month
            )

            monthly_totals = (
                yearly_data.groupby("month_number")["amount"]
                .sum()
                .reindex(range(1, 13), fill_value=0)
            )

            monthly_totals.index = [
                calendar.month_abbr[m]
                for m in range(1, 13)
            ]

            fig, ax = plt.subplots()

            monthly_totals.plot(kind="bar", ax=ax)

            ax.set_xlabel("Month")
            ax.set_ylabel("Amount (₹)")

            st.pyplot(fig)
            plt.close(fig)

            if yearly_total > 0:

                highest_month = monthly_totals.idxmax()

                st.write(
                    f"Highest spending month: **{highest_month}** "
                    f"({money(monthly_totals.max())})"
                )

            # CATEGORY SPENDING

            st.subheader("Category-wise Yearly Spending")

            category_totals = (
                yearly_data.groupby("category")["amount"]
                .sum()
                .sort_values(ascending=False)
            )

            if not category_totals.empty:

                fig, ax = plt.subplots()

                category_totals.plot(kind="bar", ax=ax)

                ax.set_xlabel("Category")
                ax.set_ylabel("Amount (₹)")

                st.pyplot(fig)
                plt.close(fig)

            # YEARLY REPORT

            st.subheader("Yearly Expense Report")

            report = yearly_data.copy()

            report["date"] = (
                report["date"].dt.strftime("%Y-%m-%d")
            )

            st.download_button(
                "📥 Download Yearly Report",
                data=report.to_csv(index=False).encode("utf-8"),
                file_name=f"ExpenseEase_{selected_year}_Yearly_Report.csv",
                mime="text/csv"
            )


# ==========================================
# SMART RECOMMENDATIONS
# ==========================================

elif page == "Smart Recommendations":

    st.title("💡 Smart Spending Recommendations")

    if df.empty:

        st.info("Add expenses to generate recommendations.")

    else:

        today = date.today()

        current_data = df[
            (df["date"].dt.month == today.month) &
            (df["date"].dt.year == today.year)
        ].copy()

        if current_data.empty:

            st.info("No expenses recorded this month.")

        else:

            category_totals = (
                current_data.groupby("category")["amount"]
                .sum()
                .sort_values(ascending=False)
            )

            total = current_data["amount"].sum()

            highest_category = category_totals.idxmax()
            highest_amount = category_totals.max()

            st.metric(
                "Total Spending This Month",
                money(total)
            )

            st.subheader("Your Spending Breakdown")

            st.bar_chart(category_totals)

            # PERSONALIZED SUGGESTIONS

            st.subheader("💜 Personalized Suggestions")

            st.markdown("""
            <style>
            .recommendation-box {
                background-color: #F3E8FF;
                color: #2E104D !important;
                padding: 18px;
                border-radius: 12px;
                border: 2px solid #C084FC;
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 12px;
            }
            </style>
            """, unsafe_allow_html=True)

            st.markdown(
                f'<div class="recommendation-box">'
                f'Your highest spending category is '
                f'{highest_category}, with expenses of '
                f'{money(highest_amount)}.'
                f'</div>',
                unsafe_allow_html=True
            )

            if highest_amount / total >= 0.40:

                suggestion = (
                    f"You are spending more than 40% of your money "
                    f"on {highest_category}. Try reducing this category."
                )

            else:

                suggestion = (
                    "Your spending is distributed across different categories."
                )

            st.markdown(
                f'<div class="recommendation-box">'
                f'{suggestion}'
                f'</div>',
                unsafe_allow_html=True
            )

            average = total / len(current_data)

            st.markdown(
                f'<div class="recommendation-box">'
                f'Your average expense per transaction is '
                f'{money(average)}.'
                f'</div>',
                unsafe_allow_html=True
            )

            if average > 500:

                average_suggestion = (
                    "Consider reviewing larger purchases before spending."
                )

            else:

                average_suggestion = (
                    "Your average transaction amount is relatively low."
                )

            st.markdown(
                f'<div class="recommendation-box">'
                f'{average_suggestion}'
                f'</div>',
                unsafe_allow_html=True
            )
# ==========================================
# SAVINGS GOALS
# ==========================================

elif page == "Savings Goals":

    st.title("🎯 Savings Goal Tracker")

    st.write(
        "Plan your savings, set targets and achieve your financial goals!"
    )

    # CREATE A NEW GOAL

    st.subheader("➕ Create a New Savings Goal")

    with st.form("savings_goal_form"):

        goal_name = st.text_input(
            "Goal Name",
            placeholder="Example: Buy a Laptop"
        )

        target_amount = st.number_input(
            "Target Amount (₹)",
            min_value=1.0,
            value=50000.0,
            step=500.0
        )
        name = goal_name
        st.markdown(
    f"""
    <div style="
        background-color: #F5F0FF;
        padding: 22px;
        border-radius: 14px;
        border: 2px solid #C4B5FD;
        margin-bottom: 12px;
        color: #24123D;
    ">

        <h3 style="color:#4C1D75;">
            🎯 {name}
        </h3>

        <p style="color:#24123D; font-weight:600;">
            Target Amount: ₹{target:,.2f}
        </p>

        <p style="color:#24123D; font-weight:600;">
            Amount Saved: ₹{saved:,.2f}
        </p>

        <p style="color:#24123D; font-weight:600;">
            Remaining: ₹{remaining:,.2f}
        </p>

        <p style="color:#24123D; font-weight:600;">
            Target Date: {deadline}
        </p>

        <h3 style="color:#166534;">
            {progress * 100:.1f}% Completed
        </h3>

    </div>
    """,
    unsafe_allow_html=True
)
        

        target_date = st.date_input(
           "Choose your target date",
           label_visibility="collapsed"
        )
 
        

        create_goal = st.form_submit_button(
            "Create Savings Goal"
        )

        if create_goal:

            if goal_name.strip():

                with get_connection() as conn:

                    conn.execute(
                        """
                        INSERT INTO savings_goals
                        (goal_name, target_amount, saved_amount, target_date)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            goal_name.strip(),
                            target_amount,
                            0,
                            str(target_date)
                        )
                    )

                st.success("Your savings goal has been created!")
                st.rerun()

            else:

                st.error("Please enter a goal name.")

    st.divider()

    # DISPLAY SAVINGS GOALS

    st.subheader("💜 Your Savings Goals")

    with get_connection() as conn:

        goals = conn.execute(
            """
            SELECT id, goal_name, target_amount,
                   saved_amount, target_date
            FROM savings_goals
            ORDER BY id DESC
            """
        ).fetchall()

    if not goals:

        st.info("You haven't created any savings goals yet.")

    else:

        for goal in goals:

            goal_id = goal[0]
            name = goal[1]
            target = float(goal[2])
            saved = float(goal[3] or 0)
            deadline = goal[4]

            remaining = max(target - saved, 0)

            progress = min(saved / target, 1.0)

            st.markdown(
                f"""
                <div style="
                    background-color: #F3E8FF;
                    padding: 20px;
                    border-radius: 14px;
                    border: 2px solid #C084FC;
                    margin-bottom: 10px;
                ">
                    <h3 style="color:#542583;">
                        🎯 {name}
                    </h3>

                    <p style="color:#2E104D;">
                        Target Amount: ₹{target:,.2f}
                    </p>

                    <p style="color:#2E104D;">
                        Amount Saved: ₹{saved:,.2f}
                    </p>

                    <p style="color:#2E104D;">
                        Remaining: ₹{remaining:,.2f}
                    </p>

                    <p style="color:#2E104D;">
                        Target Date: {deadline}
                    </p>

                    <h3 style="color:#15803D;">
                        {progress * 100:.1f}% Completed
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(progress)

            # UPDATE SAVINGS

            with st.form(f"update_goal_{goal_id}"):

                new_saved = st.number_input(
                    "Enter Total Amount Saved (₹)",
                    min_value=0.0,
                    value=saved,
                    step=500.0,
                    key=f"saved_{goal_id}"
                )

                update_goal = st.form_submit_button(
                    "Update Savings"
                )

                if update_goal:

                    with get_connection() as conn:

                        conn.execute(
                            """
                            UPDATE savings_goals
                            SET saved_amount = ?
                            WHERE id = ?
                            """,
                            (new_saved, goal_id)
                        )

                    st.success("Savings updated successfully!")
                    st.rerun()

            if saved >= target:

                st.success(
                    "🎉 Congratulations! You achieved your savings goal!"
                )

            st.divider()

# ==========================================
# FOOTER
# ==========================================

st.sidebar.markdown("---")

st.sidebar.caption(
    "Made with 💜 using Python and Streamlit"
)
