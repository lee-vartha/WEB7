import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { DonorDashboardComponent } from './components/donor-dashboard/donor-dashboard.component';
import { BeneficiaryDashboardComponent } from './components/beneficiary-dashboard/beneficiary-dashboard.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'donor', component: DonorDashboardComponent },
  { path: 'beneficiary', component: BeneficiaryDashboardComponent },
  { path: '', redirectTo: 'login', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
