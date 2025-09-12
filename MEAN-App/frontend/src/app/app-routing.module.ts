import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RegisterComponent } from './components/register/register.component';
import { LoginComponent } from './components/login/login.component';
import { DonorDashboardComponent } from './components/donor-dashboard/donor-dashboard.component';
import { BeneficiaryDashboardComponent } from './components/beneficiary-dashboard/beneficiary-dashboard.component';

const routes: Routes = [
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'donor-dashboard', component: DonorDashboardComponent },
  { path: 'beneficiary-dashboard', component: BeneficiaryDashboardComponent },
  { path: '', redirectTo: '/register', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
