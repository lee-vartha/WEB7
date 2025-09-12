// importing necessary modules and services (for angular component, api service, etc.)
import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

// defining that the component is the donor dashboard with its selector and template
@Component({
  selector: 'app-donor-dashboard',
  templateUrl: './donor-dashboard.component.html',
  styleUrls: ['./donor-dashboard.component.css']
})
// exporting the DonorDashboardComponent class implementing OnInit interface
export class DonorDashboardComponent implements OnInit {
  products: any[] = [];
  form = { name: '', description: '', cost: 0 };
  msg = '';

  constructor(private api: ApiService) {}

  // on load, fetch the products
  ngOnInit(): void {
    this.loadProducts();
  }

  // load the products
  loadProducts() {
    this.api.getProducts().subscribe({
      next: (res) => (this.products = res),
      error: () => (this.products = [])
    });
  }

  // adding a product
  addProduct() {
    // if this form is not filled properly, show message and return
    if (!this.form.name || !this.form.description || !this.form.cost) {
      this.msg = 'Please fill all fields';
      return;
    }

    // add the product using the api service
    this.api.addProduct(this.form).subscribe({
      next: (res) => {
        this.msg = 'Product added!';
        this.loadProducts();
        this.form = { name: '', description: '', cost: 0 }; // reset form
      },
      error: (err) => {
        this.msg = err.error?.msg || 'Error adding product';
      }
    });
  }
}
