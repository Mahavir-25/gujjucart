 document.addEventListener('DOMContentLoaded', () => {
    const wishlistToggle = document.getElementById("wishlistToggle");
    const wishlistSidebar = document.getElementById("miniWishlistSidebar");
    const closeWishlist = document.getElementById("closeWishlist");
    const wishlistCountEl = document.getElementById("wishlist-count");
    const cartCountEl = document.getElementById("cart-count");
    const wishlistItems = document.getElementById("wishlist-items");
    const slider = document.getElementById('heroSlider');
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prevSlide');
    const nextBtn = document.getElementById('nextSlide');
    const dots = document.querySelectorAll('[data-slide]');
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.forEach(toastEl => {
      const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
      toast.show();
    });


    /* ✅ 1. Helper Function: Get CSRF Token */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /* ✅ 2. Sidebar Toggle + Fetch Wishlist */
    if (wishlistToggle && wishlistSidebar && closeWishlist) {
        wishlistToggle.addEventListener("click", () => {
            wishlistSidebar.classList.toggle("translate-x-full");
            wishlistSidebar.classList.toggle("translate-x-0");

            // Fetch updated wishlist only when sidebar opens
            if (wishlistSidebar.classList.contains("translate-x-0")) {
                fetchUpdatedWishlist();
            }
        });

        closeWishlist.addEventListener("click", () => {
            wishlistSidebar.classList.remove("translate-x-0");
            wishlistSidebar.classList.add("translate-x-full");
        });

        // Optional: close sidebar if clicked outside
        document.addEventListener("click", (e) => {
            if (!wishlistSidebar.contains(e.target) && !wishlistToggle.contains(e.target)) {
                wishlistSidebar.classList.remove("translate-x-0");
                wishlistSidebar.classList.add("translate-x-full");
            }
        });
    }

    /* ✅ 3. Fetch Latest Wishlist from Server */
    function fetchUpdatedWishlist() {
    
        fetch(`/get-wishlist/`)
            .then(res => res.json())
            .then(data => {
                updateWishlistSidebar(data.wishlist);
                if (wishlistCountEl) wishlistCountEl.textContent = data.wishlist.length;
            })
            .catch(err => console.error("Error fetching wishlist:", err));
    }

    /* ✅ 4. Render Wishlist Items Dynamically */
    function updateWishlistSidebar(wishlist) {
        wishlistItems.innerHTML = "";
        if (wishlist.length === 0) {
            wishlistItems.innerHTML = `<p class="text-gray-500 text-sm text-center">No items in wishlist.</p>`;
        } else {
            wishlist.forEach(item => {
                wishlistItems.innerHTML += `
                    <div class="flex items-center space-x-2 hover:bg-sky-200 rounded-lg p-1.5 transition cursor-pointer">
                        <img src="${item.image}" alt="${item.name}" class="w-10 h-10 rounded object-cover">
                        <div>
                            <p class="font-medium text-gray-800 truncate text-sm">${item.name}</p>
                            <p class="text-xs text-gray-600">₹${item.price}</p>
                        </div>
                    </div>
                `;
            });
        }
    }
      
 if (slider && slides.length > 0 && prevBtn && nextBtn && dots.length > 0) {
    let currentIndex = 0;
    const totalSlides = slides.length;
    let autoSlideInterval;

    // Show slide by index
    function showSlide(index) {
        currentIndex = (index + totalSlides) % totalSlides;
        slider.style.transform = `translateX(-${currentIndex * 100}%)`;

        // Update dots
        dots.forEach((dot, i) => {
            if (i === currentIndex) {
                dot.classList.add('bg-white');
                dot.classList.remove('bg-white/50');
            } else {
                dot.classList.remove('bg-white');
                dot.classList.add('bg-white/50');
            }
        });
    }

    // Next and previous buttons
    nextBtn.addEventListener('click', () => {
        showSlide(currentIndex + 1);
        resetAutoSlide();
    });

    prevBtn.addEventListener('click', () => {
        showSlide(currentIndex - 1);
        resetAutoSlide();
    });

    // Dot click navigation
    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            showSlide(i);
            resetAutoSlide();
        });
    });

    // Auto slide function
    function startAutoSlide() {
        autoSlideInterval = setInterval(() => {
            showSlide(currentIndex + 1);
        }, 5000); // every 5 seconds
    }

    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        startAutoSlide();
    }

    // Initialize slider
    showSlide(0);
    startAutoSlide();
}
 


    /* ✅ 5. Wishlist Heart (Add/Remove) with Live Count Update */
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    wishlistButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (button.dataset.bsToggle === "modal") return; // Skip for guest users

            const productId = button.dataset.productId;
            const icon = button.querySelector('i');

            fetch(`/toggle-wishlist/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'added') {
                    icon.classList.remove('far', 'text-gray-400');
                    icon.classList.add('fas', 'text-red-500');
                } else if (data.status === 'removed') {
                    icon.classList.remove('fas', 'text-red-500');
                    icon.classList.add('far', 'text-gray-400');
                }

                if (wishlistCountEl && data.wishlist_count !== undefined) {
                    wishlistCountEl.textContent = data.wishlist_count;
                }

                // Refresh sidebar dynamically after any toggle
                fetchUpdatedWishlist();
            })
            .catch(err => console.error('Wishlist toggle error:', err));
        });
    });
});
