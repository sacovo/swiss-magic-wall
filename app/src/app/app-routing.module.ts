import { NgModule } from '@angular/core'
import { Routes, RouterModule } from '@angular/router'
import {AboutComponent} from './about/about.component'
import { VotationDatesComponent } from './votation-dates/votation-dates.component'
import { VotationDetailComponent } from './votation-detail/votation-detail.component'

const routes: Routes = [
  {
    path: 'date',
    component: VotationDatesComponent,
  },
  { path: 'date/:id', component: VotationDatesComponent },
  { path: 'about', component: AboutComponent },
  { path: 'votation/:id', component: VotationDetailComponent },
  { path: '', redirectTo: '/date', pathMatch: 'full'},
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
