import { HttpClient } from '@angular/common/http'
import { Injectable } from '@angular/core'
import { Observable, of } from 'rxjs'
import { VotationDate } from './votation'

@Injectable({
  providedIn: 'root',
})
export class VotationDateService {
  apiURL = '/api/dates/'

  constructor(private http: HttpClient) {}

  getVotationDates(): Observable<VotationDate[]> {
    return this.http.get<VotationDate[]>(this.apiURL)
  }

  getVotationDate(id: number): Observable<VotationDate> {
    return this.http.get<VotationDate>(this.apiURL + id + '/')
  }
}
