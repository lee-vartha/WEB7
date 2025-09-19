// importing necessary modules and services (for angular component, api service, router, etc.)
import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { Router } from '@angular/router';

// setting up the component with its selector and template
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']

})

// exporting the LoginComponent class
export class LoginComponent {
  form = { email: '', password: '' };
  msg = '';

  constructor(private api: ApiService, private router: Router) {}

  // login method to authenticate user
  login() {
    this.api.login(this.form).subscribe({
      next: (res) => {
        // Save token and user
        localStorage.setItem('token', res.token);
        localStorage.setItem('user', JSON.stringify(res.user));
        this.msg = 'Login successful!';

        // Navigate by role
        if (res.user.role === 'donor') {
          this.router.navigate(['/donor-dashboard']);
        } else {
          this.router.navigate(['/beneficiary-dashboard']);
        }
      },
      error: (err) => {
        this.msg = err.error?.msg || 'Invalid credentials';
      }
    });
  }
}
