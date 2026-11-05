// 1. Database creation
use("ecommerce");

// 2. + 3. Collections are created on insertion
db.users.insertMany([
  { name: "Alice", age: 25, city: "Paris" },
  { name: "Bob", age: 32, city: "Lille" },
  { name: "Chloe", age: 28, city: "Paris" }
]);

db.products.insertMany([
  { name: "Laptop", price: 899, category: "Electronics" },
  { name: "Mouse", price: 25, category: "Electronics" },
  { name: "Desk chair", price: 120, category: "Furniture" },
  { name: "Notebook", price: 5, category: "Stationery" }
]);

db.orders.insertOne({
  user: "Alice",
  products: [{ name: "Laptop", price: 899 }, { name: "Mouse", price: 25 }],
  total: 924
});

// 4. Queries
printjson(db.users.find().toArray());
printjson(db.products.find({ price: { $gt: 50 } }).toArray());
printjson(db.users.find({ city: "Paris" }).toArray());
printjson(db.orders.find().toArray());

// 5. Update
db.users.updateOne({ name: "Bob" }, { $set: { age: 33 } });

// 6. Deletion
db.products.deleteOne({ name: "Notebook" });
