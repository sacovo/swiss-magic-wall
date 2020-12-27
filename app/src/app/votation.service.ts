import { HttpClient } from '@angular/common/http'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import { environment } from 'src/environments/environment'
import { Votation, VotationDataSeries } from './votation'

@Injectable({
  providedIn: 'root',
})
export class VotationService {
  apiURL = environment.apiUrl + 'votation/'

  constructor(private http: HttpClient) {}

  getVotation(id: number | string): Observable<Votation> {
    return this.http.get<Votation>(this.apiURL + id + '/')
  }

  getVotationStats(id: number | string, cantonId?: number | string): Observable<VotationDataSeries[]> {
    if (cantonId) {
      return this.http.get<VotationDataSeries[]>(this.apiURL + id + '/stats/' + cantonId + "/")
    }
    return this.http.get<VotationDataSeries[]>(this.apiURL + id + '/stats/')
  }
}
