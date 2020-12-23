import { BrowserModule } from '@angular/platform-browser'
import { LOCALE_ID, NgModule } from '@angular/core'
import { HttpClientModule } from '@angular/common/http'

import { MatCardModule } from '@angular/material/card'
import { MatSidenavModule } from '@angular/material/sidenav'
import { MatIconModule } from '@angular/material/icon'
import { MatToolbarModule } from '@angular/material/toolbar'
import { NgxChartsModule } from '@swimlane/ngx-charts'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { MatButtonModule } from '@angular/material/button'
import { MatListModule } from '@angular/material/list'
import { MatTabsModule } from '@angular/material/tabs'
import { TableModule } from 'primeng/table'
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner'

import { AppRoutingModule } from './app-routing.module'
import { AppComponent } from './app.component'
import { VotationDatesComponent } from './votation-dates/votation-dates.component'
import { SimpleVotationComponent } from './simple-votation/simple-votation.component'
import { VotationDetailComponent } from './votation-detail/votation-detail.component'
import { MapComponent } from './map/map.component'
import { VotationDateDetailComponent } from './votation-date-detail/votation-date-detail.component'
import { AboutComponent } from './about/about.component'
import { VotationTableComponent } from './votation-table/votation-table.component'
import { registerLocaleData } from '@angular/common'
import localeDECH from '@angular/common/locales/de-CH'
registerLocaleData(localeDECH)

@NgModule({
  declarations: [
    AppComponent,
    VotationDatesComponent,
    SimpleVotationComponent,
    VotationDetailComponent,
    MapComponent,
    VotationDateDetailComponent,
    AboutComponent,
    VotationTableComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgxChartsModule,
    BrowserAnimationsModule,
    MatCardModule,
    MatSidenavModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatListModule,
    MatTabsModule,
    TableModule,
    MatProgressSpinnerModule,
  ],
  providers: [{ provide: LOCALE_ID, useValue: 'de-CH' }],
  bootstrap: [AppComponent],
})
export class AppModule {}
