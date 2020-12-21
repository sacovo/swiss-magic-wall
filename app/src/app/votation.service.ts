import { HttpClient } from '@angular/common/http'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import { Votation } from './votation'

@Injectable({
  providedIn: 'root',
})
export class VotationService {
  apiURL = '/api/votation/'

  constructor(private http: HttpClient) {}

  getVotation(id: number | string): Observable<Votation> {
    return this.http.get<Votation>(this.apiURL + id + '/')
  }
}
