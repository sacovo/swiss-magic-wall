import { HttpClient } from '@angular/common/http'
import { Injectable } from '@angular/core'
import { Observable, of } from 'rxjs'
import { environment } from 'src/environments/environment'
import { RelatedResult, Votation, VotationDataSeries } from './votation'

@Injectable({
  providedIn: 'root',
})
export class VotationService {
  apiURL = environment.apiUrl + 'votation/'

  constructor(private http: HttpClient) {}

  getVotation(id: number | string): Observable<Votation> {
    return this.http.get<Votation>(this.apiURL + id + '/')
  }

  getVotationStats(
    id: number | string,
    cantonId?: number | string
  ): Observable<VotationDataSeries[]> {
    if (cantonId) {
      return this.http.get<VotationDataSeries[]>(
        this.apiURL + id + '/stats/' + cantonId + '/'
      )
    }
    return this.http.get<VotationDataSeries[]>(this.apiURL + id + '/stats/')
  }

  getVotationStatsCommune(
    id: number | string,
    communeId: number | string
  ): Observable<VotationDataSeries[]> {
    return this.http.get<VotationDataSeries[]>(
      this.apiURL + id + '/stats/commune/' + communeId + '/'
    )
  }

  getRelatedResults(id: number | string): Observable<RelatedResult[]> {
    return this.http.get<RelatedResult[]>(this.apiURL + id + '/rel/')
  }

  getRelatedCantonResults(
    id: number | string,
    cantonId: number | string
  ): Observable<RelatedResult[]> {
    return this.http.get<RelatedResult[]>(
      this.apiURL + id + '/rel/canton/' + cantonId + '/'
    )
  }

  getRelatedCommuneResults(
    id: number | string,
    communeId: number | string
  ): Observable<RelatedResult[]> {
    return this.http.get<RelatedResult[]>(
      this.apiURL + id + '/rel/commune/' + communeId + '/'
    )
  }
}
