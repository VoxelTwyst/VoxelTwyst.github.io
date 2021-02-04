# Per-pixel similarity
Effectively, PIXIM works by matching each pixel in one image with a pixel in the other. It then estimates that pixel's distance from the camera based on how far apart the matching pixels are, emulating real-life binocular vision.

What it actually does is:
1. Virtually lay the two images on top of eachother.
2. By passing each matching pair of pixels into a function which takes two colours and returns a value corresponding to how "similar" they are, convert the pair of images to a single, greyscale image.
3. Move one of the images to the side to simulate a change in depth. Repeat step 2.
4. Continue repeating until the images no longer overlap.

You now have a set of "similarity maps", one for each possible depth value.

5. Let each pixel's estimated depth be the depth at which it has the highest similarity value. Compile these into a final greyscale image.
    **Special case**: If there is a tie for the highest similarity, let the pixel's estimated depth be the average of the tied depths.

Note that steps 2-4, and step 5, can be executed for multiple pixels at once using a GPU.

## Main algorithm
```
SUBROUTINE pixim(left [image from left camera], right [image from right camera])
    // Images are known to be the same size. Create variables for that size for ease of access.
    width <- left.width
    height <- left.height

    // Create empty array of similarity maps.
    similarity_maps <- [3d empty array, with dimensions width * width * height]

    // Populate the array
    FOREACH depth [values between 0 and width], x [also values between 0 and width], y [values between 0 and height]
        similarity_maps[depth, x, y] = similarity( left.getPixel(x + depth, y) , right.getPixel(x, y) )
        // see below for similarity functions

    // Create empty depthmap
    depth_map <- [2d empty array, with dimensions width * height]

    // Populate the array
    FOREACH x, y
        estimated_depth <- 0
        number_most_similar [the number of depths which share the highest similarity value] <- 0

        FOREACH depth, similarity
            IF similarity > similarity_maps[estimated_depth, x, y]
                estimated_depth <- depth
                number_most_similar <- 1
            
            OTHERWISE, IF similarity = similarity_maps[estimated_depth, x, y]
                // Work out the new average, incorporating the new value
                estimated_depth <- (estimated_depth * number_most_similar) + depth
                INCREMENT number_most_similar
                estimated_depth <- estimated_depth / number_most_similar

        depth_map[x, y] = estimated_depth

    RETURN depth_map
```

## Similarity functions
PIXIM requires a "similarity function", which determines how "similar" two colours are, to generate its similarity maps. There are more than one possible ways of doing this, however. Here are some of my ideas:

\(All colours are HSV, with values between 0 and 1. This is used over RGB to better match the way humans percieve colour.\)
### Inverse difference
1. Find the absolute difference (|a-b|) between the H, S and V of each colour.
2. Subtract them from 1.
3. Find the average of the resulting values.

```
SUBROUTINE similarity(a [colour], b [different colour])
    h_similarity <- 1 - Abs(a.h - b.h)
    s_similarity <- 1 - Abs(a.s - b.s)
    v_similarity <- 1 - Abs(a.v - b.v)

    RETURN (h_similarity + s_similarity + v_similarity) / 3
```
You could consider weighting the average calculation in favour of hue, since this is likely to be the most different between different objects.

#### Problems
- Does not consider that hue is circular. According to this algorithm, red and hot pink are less similar than red and cyan.

### Circular inverse difference
The same as regular inverse difference, but for hue, instead of the usual absolute difference calculation:
1. Find the absolute difference between the colours' H values.
2. Find the absolute difference between the first colour's hue and 1 - (the second colour's hue)
3. Continue, using whichever of the above is smaller as the value of the hue difference.

```
SUBROUTINE similarity(a, b)
    h_difference <- MINIMUM( Abs(a.h - b.h) , Abs(a.h - (1 - b.h)) )
    
    h_similarity <- 1 - h_difference
    s_similarity <- 1 - Abs(a.s - b.s)
    v_similarity <- 1 - Abs(a.v - b.v)

    RETURN (h_similarity + s_similarity + v_similarity) / 3
```

# Median filter
I did not come up with the idea for this algorithm, but I predict that it would improve the quality of my depthmaps.

It is not a depthmap generation algorithm in its own right. Instead, it is a process to be applied to the original images, or to the depthmap, before or after the depthmap is generated. It is selected to work alongside PIXIM, whose main weakness is its lack of awareness of the context surrounding each pixel.

It simply lets each pixel's colour be the median of the surrounding pixels' colours, from within a certain radius.

This can also be sped up using a GPU.

Here is the pseudocode for a greyscale image. For a coloured image, simply split apart the image into its components, leaving you with 3 separate greyscale images.

```
SUBROUTINE median(array)
    array <- sort(array)
    IF array.length MOD 2 = 1
        RETURN array[array.length DIV 2]
    OTHERWISE
        RETURN (array[array.length DIV 2 - 1] + array[array.length DIV 2]) DIV 2


SUBROUTINE median_filter(image, radius)
    // Build array of relative coordinates to consider for each pixel
    CONSTANT look_at <- [the set of pairs of coordinates (x, y), where -radius <= x <= radius and -radius <= y <= radius]

    width <- image.width
    height <- image.height

    // Initialise output array
    out <- [2d empty array, with dimensions width * height]

    // Populate output array
    FOREACH x [0 to width], y [0 to height]
        // Initialise array of neighbouring colours
        neighbours <- [1d array with the same length as look_at]

        FOREACH plus_x, plus_y IN look_at
            APPEND image[x + plus_x, y + plus_y] TO neighbours

        out[x, y] <- median(neighbours)
    
    RETURN out
```
## Problems
- The median-finding subroutine is not very fast. I will need to create a faster one.

### Finding the Median
I have done some research into median-finding algorithms. One which has a good balance between speed and simplicity (it is O(n) on average) is called Quickselect. It looks like this:

```
SUBROUTINE quickselect(list, index)
   // Returns the <index>th greatest element of <list>. //
   
   IF LENGTH(list) = 1 THEN   // Base case - for any valid <index> (ie, index = 0),
                              // the <index>th greatest element of a length-1 list is its only element.
      return list[0]
   ENDIF
   
   pivot = list[LENGTH(list) // 2]
   
   lower = {all values less than <pivot> in <list>}
   higher = {all values greater than <pivot> in <list>}
   equal = {all values equal to <pivot> in <list>}
   
   IF pivot < LENGTH(lower) THEN
      RETURN quickselect(lower, index)
   ELSE IF index < LENGTH(lower) + LENGTH(equal)
      RETURN pivot   // We accidentally found it
   ELSE
      RETURN quickselect(higher, pivot - LENGTH(lower) - LENGTH(equal))
   ENDIF
ENDSUBROUTINE
```