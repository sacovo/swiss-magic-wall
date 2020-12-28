import { Component } from '@angular/core'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less'],
})
export class AppComponent {

  fullScreen: boolean = false;

  public constructor() {}

  title = 'Magic Wall'

  toggleFullscreen(): void {
    const elem = document.documentElement

    if (this.fullScreen) {
      document.exitFullscreen()
      this.fullScreen = false;
    } else if (elem.requestFullscreen) {
      elem.requestFullscreen()
      this.fullScreen = true
    }
  }
}
