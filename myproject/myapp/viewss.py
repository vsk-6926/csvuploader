import pandas as pd
from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import Transaction

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)
            df = df.head(60)  # Select the first 60 rows

            # Check if all required columns are present
            required_columns = ['Invoice ID', 'Product line', 'Unit price', 'Quantity', 'Tax', 'Total', 'Date', 'Time']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                error_message = f"The following columns are missing in the CSV file: {', '.join(missing_columns)}"
                return render(request, 'upload_csv.html', {'form': form, 'error_message': error_message})

            # Save the selected data to the database
            for _, row in df.iterrows():
                transaction = Transaction(
                    invoice_id=row['Invoice ID'],
                    product_line=row['Product line'],
                    unit_price=row['Unit price'],
                    quantity=row['Quantity'],
                    total=row['Total'],
                    date=row['Date'],
                    time=row['Time']
                )
                transaction.save()
                transactions.append(transaction)
            
            Transaction.objects.bulk_create(transactions)

            return redirect('transactions')

    else:
        form = CSVUploadForm()

    return render(request, 'upload_csv.html', {'form': form})

def transactions(request):
    transactions = Transaction.objects.filter(product_line='Health and beauty')[:60]
    return render(request, 'transactions.html', {'transactions': transactions})

