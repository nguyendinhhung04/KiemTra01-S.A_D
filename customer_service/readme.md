# System Design

## API Gateway

### Responsibilities
- Single entry point for all client requests
- Route requests to appropriate services

### Routing
- `/api/customers/*` → customer_service
- `/api/staff/*` → staff_service
- `/api/laptops/*` → laptop_service
- `/api/mobiles/*` → mobile_service

### Authentication (Simple)
- User logs in via customer_service or staff_service
- Service validates username/password
- Return true/false
- Client stores login state (session / cookie)
- API Gateway forwards request without JWT validation

---

## customer_service

### Model
- **customer**: id, name, phone, email, username, password
- **cart**: id, customer_id
- **cart_item**: id, item_id, cart_id, quantity, product_type (MOBILE | LAPTOP)

### Constraints
- One customer has exactly one cart
- One cart can contain multiple items

### API
- **Register**
  - Input: name, phone, email, username, password
  - Output: created customer with id
  - Logic: create customer → automatically create cart

- **Login**
  - Input: username, password
  - Output:
    - true → redirect to Home page
    - false → show error message

- **Add to cart**
  - Input: item_id, product_type

### UI
- Register page
- Login page
- Home page
- Cart page

### Database
- MySQL

---

## staff_service

### Model
- **staff**: staff_id, name, phone, email, username, password, role

### API
- **Login**
  - Input: username, password
  - Output:
    - true → redirect to Dashboard
    - false → show error message

### UI
- Dashboard page (welcome message + navbar with Laptop and Mobile)
- Laptop page:
  - Product list
  - Edit button → open edit form
  - Add button → open create form
- Mobile page:
  - Product list
  - Edit button → open edit form
  - Add button → open create form

### Database
- MySQL

---

## laptop_service

### Model
- **laptop**: id, name, properties (string), price, discount, manufacturer_id, category_id, ram, CPU, GPU, screen
- **manufacturer**: id, name
- **category**: id, name

### API
- Get list of laptops
- Create new laptop
- Update laptop

### Database
- PostgreSQL

---

## mobile_service

### Model
- **mobile**: id, name, price, discount, manufacturer_id, category_id, ram, CPU, GPU, camera
- **manufacturer**: id, name
- **category**: id, name

### API
- Get list of mobiles
- Create new mobile
- Update mobile

### Database
- PostgreSQL