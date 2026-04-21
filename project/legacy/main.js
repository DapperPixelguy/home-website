async function typewrite() {
          let elem = document.getElementById('Username')
          let text = elem.innerText
          let count = 0
          elem.innerText = '';
          for (; count <= text.length; count++){
            await new Promise(resolve => setTimeout(resolve, 120))
            elem.innerText = text.slice(0,count)
          }
          await new Promise(resolve => setTimeout(resolve, 3000))
          elem.style.animationIterationCount = 1;
          // elem.addEventListener('animationend', () => {elem.style.animation = 'none'})
      }

        function tro() {
            document.getElementById('InfoImg').src = 'assets/the_tro.gif'
          }

        function untro() {
            document.getElementById('InfoImg').src = 'assets/info.png'

        }

var introText = document.getElementById('IntroText');
        var gradTop = document.getElementById('gradient-top');
        var y = document.getElementById("reveal-button")
        var username = document.getElementById("Username")
        var socialLinks = document.getElementById("social-Links")
        var device = document.getElementById("Device")
        var credit = document.getElementById("Credit")
        var time = document.getElementById('Time')
        var footer = document.getElementById('footer')
        var infoText = document.getElementById('InfoText')
        var specText = document.getElementById('SpecText')
        // Function to check and apply the class based on div width
        function checkDivWidth() {
          let details = navigator.userAgent
          let regexp = /android|iphone|kindle|ipad/i
          let isMobileDevice = regexp.test(details)

          if (isMobileDevice) {
            introText.classList.add('mobile');
            gradTop.classList.add('full-width');
            footer.classList.add('full-width')
            infoText.classList.add('mobile')
          } else {
            //var y = document.getElementById('reveal-button');
            if (introText.offsetWidth <= 722) {
              introText.classList.add('full-width');
              gradTop.classList.add('full-width');
              footer.classList.add('full-width')
            } else {
              introText.classList.remove('full-width');
              gradTop.classList.remove('full-width');
              footer.classList.remove('full-width')
            }
          }
        }

        // Run the function on page load and resize
        window.addEventListener('load', function() {
          y = document.getElementById('reveal-button')
        })

function revealPage() {
          let details = navigator.userAgent
          let regexp = /android|iphone|kindle|ipad/i
          let isMobileDevice = regexp.test(details)

          if (!isMobileDevice) {
            setTimeout(() => {
              introText.style.overflowX = 'auto';
            }, 2100)
            setTimeout((checkDivWidth), 1601)
            setTimeout(() => {
              window.addEventListener('load', checkDivWidth);
              window.addEventListener('resize', checkDivWidth);
              console.log('Run!')
            }, 1601)
          } else {
            introText.style.transition = 'width 0s'
            username.style.transition = 'opacity 1s 0.3s'
            socialLinks.style.transition = 'opacity 1s 0.6s'
            checkDivWidth()
          }

          introText.style.opacity = '1'
          introText.classList.add("clicked")


          setTimeout(()=>{
            username.classList.add("clicked")
            typewrite()
            }, 1000)

          socialLinks.classList.add("clicked")
          y.style.opacity = 0
          setTimeout(()=>{
          y.style.display ='none'
          }, 1400)



        }

window.addEventListener('load', function() {
          y.style.display = 'block';
          let details = navigator.userAgent
          let regexp = /android|iphone|kindle|ipad/i
          let isMobileDevice = regexp.test(details)

          if (isMobileDevice) {
            device.innerText = 'Viewing on: [Mobile]'
            device.style.fontSize = '150%'
            credit.style.fontSize = '150%'
            time.style.fontSize = '150%'
            infoText.classList.add('mobile')
            specText.classList.add('mobile')

          } else {
            device.innerText = 'Viewing on: [Desktop]'
          }
        });

function startTime() {
          const today = new Date();
          let h = today.getHours();
          let m = today.getMinutes();
          let s = today.getSeconds();
          m = checkTime(m);
          s = checkTime(s);
          document.getElementById('Time').innerHTML = h + ":" + m + ":" + s;
          setTimeout(startTime, 1000);
        }

        function checkTime(i) {
          if (i < 10) {
            i = "0" + i
          };
          return i;
        }

function showInfo() {
          var infoBox = document.getElementById('InfoBox')
          var infoButton = document.getElementById('InfoButton')
          if (infoBox.classList.contains('active')) {
            infoBox.classList.remove('active')
            infoButton.classList.remove('active')
          } else {
            infoBox.classList.add('active')
            infoButton.classList.add('active')
          }
        }

function showSpec() {

        	var specBox = document.getElementById('SpecBox')
          var specButton = document.getElementById('SpecButton')
          if (specButton.classList.contains('disabled')){
          console.log('erm what')
          	return
          console.log('the sigma')
          }
          else {
          	specButton.classList.add('disabled')
            setTimeout(() => { specButton.classList.remove('disabled')}, 3000)
            if (specBox.classList.contains('active')) {
              specBox.classList.remove('active')
              specButton.classList.remove('active')
            } else {
              specBox.classList.add('active')
              specButton.classList.add('active')
            }
          }
        }