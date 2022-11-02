 static void bubbleSortPartial(int arr[]) { 
        int i, j, temp; 
        // n is the size of the array
        int n = arr.length;
        boolean swapped; 
        for (i = 0; i < n - 2; i++){ 
            swapped = false; 
            for (j = 0; j < n - i - 1; j++){
                if (arr[j] > arr[j + 1]){ 
                    // swap arr[j] and arr[j+1] 
                    temp = arr[j]; 
                    arr[j] = arr[j + 1]; 
                    arr[j + 1] = temp; 
                    swapped = true; 
                }
            } 
  
            // IF no two elements were  
            // swapped by inner loop, then break.
            // it means the numbers are already sorted.
            if (swapped == false) 
                break; 
        }