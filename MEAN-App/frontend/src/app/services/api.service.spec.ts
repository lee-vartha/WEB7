import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private baseUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  // register a new user
  register(data: any) {
    return this.http.post(`${this.baseUrl}/auth/register`, data);
  }

  login(data: any) {
    return this.http.post(`${this.baseUrl}/auth/login`, data);
  }

  getProducts() {
    return this.http.get(`${this.baseUrl}/products`);
  }

  addProduct(data: any) {
    return this.http.post(`${this.baseUrl}/products`, data);
  }

  reserveMeal(data: any) {
    return this.http.post(`${this.baseUrl}/reservations`, data);
  }
}
