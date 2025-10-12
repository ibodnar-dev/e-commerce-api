# E-Commerce Product & Variants Database Schema

## Overview
This schema supports both simple products (single SKU) and variable products (multiple variants with different options like size/color).

---

## Database Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         PRODUCTS                             │
├─────────────────────────────────────────────────────────────┤
│ id                         UUID PRIMARY KEY                  │
│ type                       ENUM('SIMPLE', 'VARIABLE')        │
│ name                       VARCHAR(255) NOT NULL             │
│ slug                       VARCHAR(255) UNIQUE NOT NULL      │
│ description                TEXT                              │
│ price                      DECIMAL(10,2) NOT NULL            │
│ sku                        VARCHAR(100) UNIQUE (SIMPLE only) │
│ status                     ENUM('DRAFT','ACTIVE','ARCHIVED') │
│ created_at                 TIMESTAMP DEFAULT NOW()           │
│ updated_at                 TIMESTAMP DEFAULT NOW()           │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 1:N (only if type = 'VARIABLE')
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      PRODUCT_VARIANTS                        │
├─────────────────────────────────────────────────────────────┤
│ id                         UUID PRIMARY KEY                  │
│ product_id                 UUID → products.id                │
│ sku                        VARCHAR(100) UNIQUE NOT NULL      │
│ name                       VARCHAR(255)                      │
│ price                      DECIMAL(10,2) (overrides parent)  │
│ is_active                  BOOLEAN DEFAULT TRUE              │
│ created_at                 TIMESTAMP DEFAULT NOW()           │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ N:M
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              VARIANT_ATTRIBUTE_VALUES                        │
├─────────────────────────────────────────────────────────────┤
│ variant_id                 UUID → product_variants.id        │
│ attribute_value_id         UUID → attribute_values.id        │
│                                                               │
│ PRIMARY KEY (variant_id, attribute_value_id)                 │
└─────────────────────────────────────────────────────────────┘
         │                                     │
         │                                     │
         ▼                                     ▼
┌──────────────────────┐          ┌──────────────────────────┐
│    ATTRIBUTES        │          │   ATTRIBUTE_VALUES       │
├──────────────────────┤          ├──────────────────────────┤
│ id       UUID PK     │          │ id        UUID PK        │
│ name     VARCHAR(50) │◄─────────┤ attribute_id  UUID       │
│ slug     VARCHAR(50) │    1:N   │ value     VARCHAR(100)   │
│                      │          │ slug      VARCHAR(100)   │
└──────────────────────┘          └──────────────────────────┘


┌─────────────────────────────────────────────────────────────┐
│                        INVENTORY                             │
├─────────────────────────────────────────────────────────────┤
│ id                         UUID PRIMARY KEY                  │
│ product_id                 UUID → products.id (SIMPLE only)  │
│ variant_id                 UUID → variants.id (VARIABLE only)│
│ quantity_available         INT DEFAULT 0                     │
│ quantity_reserved          INT DEFAULT 0                     │
│ low_stock_threshold        INT DEFAULT 10                    │
│ updated_at                 TIMESTAMP DEFAULT NOW()           │
│                                                               │
│ CONSTRAINT: (product_id IS NULL) != (variant_id IS NULL)     │
│ UNIQUE(product_id, variant_id)                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Table Descriptions

### PRODUCTS
The main product table. Contains all products regardless of whether they have variants.

**Key Points:**
- `type = 'SIMPLE'`: Product has no variants (e.g., a book). Must have `sku` filled.
- `type = 'VARIABLE'`: Product has variants (e.g., t-shirt with sizes). `sku` is NULL.
- `price`: Base price. Variants can override this.

### PRODUCT_VARIANTS
Child products that represent specific configurations (e.g., "T-Shirt - Black - Medium").

**Key Points:**
- Only exists for VARIABLE products
- Each variant has unique `sku`
- `name`: Display name like "Black / Medium"
- `price`: If NULL, uses parent product's price. If set, overrides parent price.

### ATTRIBUTES
Defines what options are available (e.g., "Color", "Size").

**Examples:**
- id: 1, name: "Color", slug: "color"
- id: 2, name: "Size", slug: "size"

### ATTRIBUTE_VALUES
Defines the actual values for each attribute (e.g., "Red", "Small").

**Examples:**
- id: 1, attribute_id: 1 (Color), value: "Black", slug: "black"
- id: 2, attribute_id: 1 (Color), value: "White", slug: "white"
- id: 3, attribute_id: 2 (Size), value: "Small", slug: "s"
- id: 4, attribute_id: 2 (Size), value: "Medium", slug: "m"

### VARIANT_ATTRIBUTE_VALUES
Junction table linking variants to their attribute values.

**Example:**
A "Black T-Shirt in Medium" variant would have two entries:
- variant_id: X, attribute_value_id: 1 (Black)
- variant_id: X, attribute_value_id: 4 (Medium)

### INVENTORY
Tracks stock levels for products or variants.

**Key Points:**
- For SIMPLE products: `product_id` is set, `variant_id` is NULL
- For VARIABLE products: `product_id` is NULL, `variant_id` is set
- `quantity_available`: Current sellable stock
- `quantity_reserved`: Stock held in carts/pending orders
- Constraint ensures either product_id OR variant_id is set, never both

---

## Example Data

### Simple Product: "Atomic Habits" Book

```sql
-- Product
INSERT INTO products (id, type, name, slug, description, price, sku, status)
VALUES (
  '550e8400-e29b-41d4-a716-446655440000',
  'SIMPLE',
  'Atomic Habits',
  'atomic-habits',
  'An Easy & Proven Way to Build Good Habits',
  16.99,
  'BOOK-AH-001',
  'ACTIVE'
);

-- Inventory (linked to product_id)
INSERT INTO inventory (product_id, variant_id, quantity_available)
VALUES (
  '550e8400-e29b-41d4-a716-446655440000',
  NULL,
  50
);
```

### Variable Product: "Organic Cotton T-Shirt"

```sql
-- 1. Parent Product (no SKU)
INSERT INTO products (id, type, name, slug, description, price, sku, status)
VALUES (
  '660e8400-e29b-41d4-a716-446655440001',
  'VARIABLE',
  'Organic Cotton T-Shirt',
  'organic-cotton-tshirt',
  'Comfortable 100% organic cotton t-shirt',
  29.99,
  NULL,  -- No SKU for parent
  'ACTIVE'
);

-- 2. Attributes
INSERT INTO attributes (id, name, slug) VALUES
  ('attr-001', 'Color', 'color'),
  ('attr-002', 'Size', 'size');

-- 3. Attribute Values
INSERT INTO attribute_values (id, attribute_id, value, slug) VALUES
  ('val-001', 'attr-001', 'Black', 'black'),
  ('val-002', 'attr-001', 'White', 'white'),
  ('val-003', 'attr-002', 'Small', 's'),
  ('val-004', 'attr-002', 'Medium', 'm'),
  ('val-005', 'attr-002', 'Large', 'l');

-- 4. Variants (Black/Small, Black/Medium, White/Small, etc.)
INSERT INTO product_variants (id, product_id, sku, name) VALUES
  ('var-001', '660e8400-...', 'TSHIRT-BLK-S', 'Black / Small'),
  ('var-002', '660e8400-...', 'TSHIRT-BLK-M', 'Black / Medium'),
  ('var-003', '660e8400-...', 'TSHIRT-WHT-S', 'White / Small');

-- 5. Link variants to their attributes
INSERT INTO variant_attribute_values (variant_id, attribute_value_id) VALUES
  -- Black/Small
  ('var-001', 'val-001'),  -- Black
  ('var-001', 'val-003'),  -- Small
  -- Black/Medium
  ('var-002', 'val-001'),  -- Black
  ('var-002', 'val-004'),  -- Medium
  -- White/Small
  ('var-003', 'val-002'),  -- White
  ('var-003', 'val-003');  -- Small

-- 6. Inventory per variant
INSERT INTO inventory (product_id, variant_id, quantity_available) VALUES
  (NULL, 'var-001', 12),  -- Black/Small: 12 units
  (NULL, 'var-002', 25),  -- Black/Medium: 25 units
  (NULL, 'var-003', 8);   -- White/Small: 8 units
```

---

## Common Queries

### Get Simple Product with Stock
```sql
SELECT 
  p.*,
  i.quantity_available,
  i.quantity_reserved
FROM products p
LEFT JOIN inventory i ON i.product_id = p.id
WHERE p.id = ? AND p.type = 'SIMPLE';
```

### Get Variable Product with All Variants
```sql
-- Get parent product
SELECT * FROM products WHERE id = ? AND type = 'VARIABLE';

-- Get all variants with their attributes and stock
SELECT 
  v.id,
  v.sku,
  v.name,
  v.price,
  i.quantity_available,
  JSON_AGG(
    JSON_BUILD_OBJECT(
      'attribute', a.name,
      'value', av.value
    )
  ) as attributes
FROM product_variants v
LEFT JOIN inventory i ON i.variant_id = v.id
LEFT JOIN variant_attribute_values vav ON vav.variant_id = v.id
LEFT JOIN attribute_values av ON av.id = vav.attribute_value_id
LEFT JOIN attributes a ON a.id = av.attribute_id
WHERE v.product_id = ?
GROUP BY v.id, i.quantity_available;
```

### Get Available Attribute Options for a Product
```sql
-- Get all available colors and sizes for a product
SELECT DISTINCT
  a.name as attribute_name,
  av.value as attribute_value
FROM product_variants v
JOIN variant_attribute_values vav ON vav.variant_id = v.id
JOIN attribute_values av ON av.id = vav.attribute_value_id
JOIN attributes a ON a.id = av.attribute_id
WHERE v.product_id = ?
ORDER BY a.name, av.value;
```

### Check Stock for Specific Variant
```sql
SELECT i.quantity_available
FROM inventory i
JOIN product_variants v ON v.id = i.variant_id
JOIN variant_attribute_values vav1 ON vav1.variant_id = v.id
JOIN attribute_values av1 ON av1.id = vav1.attribute_value_id AND av1.slug = 'black'
JOIN variant_attribute_values vav2 ON vav2.variant_id = v.id
JOIN attribute_values av2 ON av2.id = vav2.attribute_value_id AND av2.slug = 'm'
WHERE v.product_id = ?;
```

---

## Business Rules

1. **Product Type Validation:**
   - SIMPLE products MUST have `sku` filled
   - VARIABLE products MUST have `sku` as NULL
   - VARIABLE products MUST have at least one variant

2. **SKU Uniqueness:**
   - All SKUs (product or variant) must be globally unique
   - Enforce with UNIQUE constraint

3. **Inventory:**
   - Either `product_id` OR `variant_id` must be set, never both
   - `quantity_available` cannot be negative
   - When stock is 0, product/variant should show as "Out of Stock"

4. **Variant Attributes:**
   - Each variant must have at least one attribute value
   - Attribute combinations must be unique per product
   - (e.g., can't have two "Black/Medium" variants)

5. **Price Inheritance:**
   - If variant price is NULL, use parent product price
   - If variant price is set, it overrides parent

6. **Product Status:**
   - DRAFT: Not visible to customers
   - ACTIVE: Available for purchase
   - ARCHIVED: Hidden, no longer sold (soft delete)

---

## Next Steps to Extend

Once you have this working, you can add:
- **Categories** (product categorization)
- **Images** (product photos)
- **Stock Movements** (audit log for inventory changes)
- **Price History** (track price changes over time)
- **Product Reviews** (customer ratings)

But start with this core schema first!
