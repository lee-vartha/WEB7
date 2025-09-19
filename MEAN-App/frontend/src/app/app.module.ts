import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';

// standalone components
import { AppComponent } from './app.component';
import { RegisterComponent } from './components/register/register.component';
import { LoginComponent } from './components/login/login.component';
import { DonorDashboardComponent } from './components/donor-dashboard/donor-dashboard.component';
import { BeneficiaryDashboardComponent } from './components/beneficiary-dashboard/beneficiary-dashboard.component';

@NgModule({
  declarations: [],

  // ✅ standalone components go here
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    AppRoutingModule,
    AppComponent,
    RegisterComponent,
    LoginComponent,
    DonorDashboardComponent,
    BeneficiaryDashboardComponent
  ],

  providers: [],
  bootstrap: [AppComponent] // still bootstraps AppComponent
})
export class AppModule {}
