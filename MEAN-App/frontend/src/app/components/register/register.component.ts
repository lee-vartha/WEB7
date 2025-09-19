import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  form: any = { name: '', email: '', password: '', role: 'beneficiary' };
  msg = '';

  constructor(private http: HttpClient, private router: Router) {}

  register() {
    this.http.post<any>('http://localhost:5000/api/auth/register', this.form)
      .subscribe({
        next: (res) => {
          // save token + user data in localStorage
          localStorage.setItem('token', res.token);
          localStorage.setItem('user', JSON.stringify(res.user));

          // redirect based on role
          if (res.user.role === 'beneficiary') {
            this.router.navigate(['/beneficiary-dashboard']);
          } else if (res.user.role === 'donor') {
            this.router.navigate(['/donor-dashboard']);
          }

        },
        error: (err) => {
          this.msg = err.error.msg || 'Registration failed';
        }
      });
  }
}
