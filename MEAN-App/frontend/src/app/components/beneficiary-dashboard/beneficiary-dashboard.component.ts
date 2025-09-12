// importing necessary modules and services (for angular component, api service, etc.)
import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

// @component decorator with metadata
@Component({
  selector: 'app-beneficiary-dashboard',
  templateUrl: './beneficiary-dashboard.component.html',
  styleUrls: ['./beneficiary-dashboard.component.css']
})
// exporting the BeneficiaryDashboardComponent class implementing OnInit interface
export class BeneficiaryDashboardComponent implements OnInit {
  products: any[] = [];
  balance: number = 0;
  msg = '';

  constructor(private api: ApiService) {}

  // angular on init lifecycle hook - means that this code runs when the component initializes
  ngOnInit(): void {
    this.loadProducts();
    this.loadProfile();
  }

// load the products from the api service
  loadProducts() {
    this.api.getProducts().subscribe({
      next: (res) => (this.products = res),
      error: () => (this.products = [])
    });
  }

  // load the user profile to get the token balance
  loadProfile() {
    this.api.getProfile().subscribe({
      next: (res) => (this.balance = res.tokenBalance),
      error: () => (this.balance = 5)
    });
  }

  // to buy product, spending tokens
  buyProduct(productId: string) {
    this.api.spendToken(productId).subscribe({
      next: (res) => {
        // means that the purchase was successful
        this.msg = res.msg;
        this.balance = res.balance; // updated balance from backend
        this.loadProducts(); // refresh list
      },
      // otherwise show error message
      error: (err) => {
        this.msg = err.error?.msg || 'Error';
      }
    });
  }
}
