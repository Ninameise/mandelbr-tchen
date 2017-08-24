# mandelbr-tchen
Dis is a Mandelbrot/Julia set viewer written in Python3. I couldn't find a good graphic package, so instead I used ASCII-art-like visualisation. It currently supports:
- grayscale visualisation
- raw colors
- mixed
- incoloring with attractor preimages (just look it up or try it out)
- real/imaginary incoloring
- different planes (Euclidean + some inversions)
- peturbation
- Julia sets

Known bugs:
- focus point goes wild when the scale is changed, will fix it at some point if I'm bored enough
- attractor preimages don't work correctly with julia sets, which they were made for

Files:
- m13.py is the main file
- mm1.py is a very minimalistic version of it, used to test out new features before they are added to the main file
