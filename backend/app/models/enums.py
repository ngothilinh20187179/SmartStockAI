from enum import Enum

class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"

class UserRole(str, Enum):
    manager = "manager"
    staff = "staff"

class SupplierStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class InvoiceStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    error = "error"

class PaymentStatus(str, Enum):
    unpaid = "unpaid"
    partially_paid = "partially_paid"
    paid = "paid"
    refunded = "refunded"

class ProductStatus(str, Enum):
    in_stock = "in_stock"
    out_of_stock = "out_of_stock"
    low_stock = "low_stock"
    discontinued = "discontinued"

class TransactionType(str, Enum):
    import_type = "import"
    export_type = "export"
    inventory_check = "inventory_check"
    adjustment = "adjustment"