frappe.pages['company-profile'].on_page_load = function(wrapper) {
	fetchData();
	new MyPage(wrapper);
}

var docName = frappe.get_route()[1];
var cus = '';
let currentTab = "details";
/////////////personal tab variables
var customer_name = '';
var mobile = '';
var address = '';
var email = '';
var reason = '';
var customerStatus = '';
var companyOwnerPic = '';
var badge = '';
/////////////personal child table tab variables
var blocs = [];
/////////////contacts variables
var contacts = [];
var customerId;
var firstName;
var lastName;
var designation;
var email;
var phone;
var emails = [];
/////////////exports tab varialbes
var dashboardListLast = [];
var dashboardListCurr = [];
var seasonName = {};
var lastSeason = {};
var currSeason = {};
/////////////products tab variables
var totalCommittees = 0;
var totalProducts = 0;
var totalCountries = 0;
var totalClusters = 0;
var productsDetails = [];
var hs_code = 0;
var custom_international_product_hs_code = 0;
var arabic_name = 0;
var english_name =0;
var scientific_arabic_name = 0;
var scientific_english_name = 0;
function fetchData() {
	// window.addEventListener('load', function() {
    //     location.reload();
    // });
	docName = frappe.get_route()[1];
	frappe.call({
		method: "barcode_aec.barcode_aec.page.company_profile.customer_profile.get_customer",
		args: {"name" : docName},
		callback: function(r) {
			cus = r.message;
			customer_name = cus.customer_name;
			mobile = cus.custom_ceo_mobile;
			address = cus.customer_primary_address ? cus.customer_primary_address : "none";
			email = cus.custom_email;
			customerStatus = cus.custom_customer_status;
			
			blocs = cus.custom_blocs_of_targeted_countries;
			if(customerStatus == 'Suspended') {
				reason = cus.custom_reason_for_susbending;
			}
			if(cus.custom_company_owners_image != null) {
				companyOwnerPic = cus.custom_company_owners_image;
			}
			if(cus.custom_attached_image !== null && cus.custom_attached_image !== "") {
				badge = `<img src=${cus.custom_attached_image} alt="avatar" class="rounded-circle">`;
			}else{
				badge = `<img src="https://eu.ui-avatars.com/api/?name=${customer_name}&size=250" alt="avatar" class="rounded-circle">`;
			}
			fetchExportsData();
			getContacts();
			get_emails();
			calculateProductsCards();
			fetchAllProductsDetails();
			render_new_design();
		}
	});
}

//page content
MyPage = Class.extend({
	init: function(wrapper) {
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'Company code : ' + docName,
			single_column: true,
		});
		//make page
		this.make();
	},
	//make page
	make: function() {
		//grab the class
		// let me = $(this);
		//push dom element to page
		$(frappe.render_template(frappe.frappe_page.body, this)).appendTo(this.page.main);
		// Set the page property in frappe.posawesome_page
        frappe.frappe_page.page = this.page;
	}
});

//html content
let body = `
<head>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
<style>
.met-profile .met-profile-main {
	display: -webkit-box;
	display: -ms-flexbox;
	display: flex;
	-webkit-box-orient: horizontal;
	-webkit-box-direction: normal;
		-ms-flex-direction: row;
			flex-direction: row;
	-webkit-box-flex: 1;
		-ms-flex: 1;
			flex: 1;
	-ms-flex-wrap: wrap;
		flex-wrap: wrap;
	-webkit-box-align: center;
		-ms-flex-align: center;
			align-items: center;
}

.met-profile .met-profile-main .met-profile-main-pic {
	position: relative;
	max-width: 128px;
	max-height: 128px;
	margin-right: 24px;
}

.met-profile .met-profile-main .met-profile-main-pic .fro-profile_main-pic-change {
	cursor: pointer;
	background-color: #4d79f6;
	border-radius: 50%;
	width: 32px;
	height: 32px;
	position: absolute;
	bottom: 4px;
	right: 4px;
	display: -webkit-box;
	display: -ms-flexbox;
	display: flex;
	-webkit-box-align: center;
		-ms-flex-align: center;
			align-items: center;
	-webkit-box-pack: center;
		-ms-flex-pack: center;
			justify-content: center;
	-webkit-box-flex: 1;
		-ms-flex: 1;
			flex: 1;
	-webkit-box-shadow: 0px 0px 20px 0px rgba(32, 41, 74, 0.05);
			box-shadow: 0px 0px 20px 0px rgba(32, 41, 74, 0.05);
	/* Apply the animation */
	animation: shine 1s infinite;
}

.met-profile .met-profile-main .met-profile-main-pic .fro-profile_main-pic-change i {
	-webkit-transition: all 0.3s;
	transition: all 0.3s;
	color: #ffffff;
	font-size: 16px;
}

.met-profile .met-profile-main .met-profile_user-detail .met-user-name {
	font-size: 24px;
	font-weight: 600;
	color: #aeb4ce;
	margin-bottom: 6px;
}

.met-profile .met-profile-main .met-profile_user-detail .met-user-name-post {
	color: #7a88af;
}

.met-profile .personal-detail li {
	color: #aeb4ce;
}

.rounded-circle {
	border-radius: 50%;
    overflow: hidden;
    width: 128px;
    height: 128px;
	border: 2px solid #fff;
	
}

.nav-link {
	background-color: #ADD8E6;
	color: #A7C7E7;
}

@keyframes shine {
	to {
		background-position-x: -200%;
	}
}
</style>

</head>
<body>
<div class="row">
<div class="col-12">
	<div class="card">
		<div class="card-body  met-pro-bg">
			<div class="met-profile shine">
				<div class="row" style="background-color: #36454F">
					<div class="col-lg-4 align-self-center mb-3 mb-lg-0">
						<div class="met-profile-main">
							<div class="met-profile-main-pic">
								<img src="userprofile.jpg" alt="" class="rounded-circle">
								<span class="fro-profile_main-pic-change shine">
									<i class="fas fa-camera"></i>
								</span>
							</div>
							<div class="met-profile_user-detail">
								<h5 class="met-user-name">${customer_name}</h5>                                                        
								<p class="mb-0 met-user-name-post">UI/UX Designer</p>
							</div>
						</div>                                                
					</div><!--end col-->
					<div class="col-lg-4 ml-auto">
						<ul class="list-unstyled personal-detail">
							<li class=""><i class="dripicons-phone mr-2 text-info font-18"></i> <b> CEO Mobile </b> : ${mobile}</li>
							<li class="mt-2"><i class="dripicons-mail text-info font-18 mt-2 mr-2"></i> <b> Email </b> : ${email}</li>
							<li class="mt-2"><i class="dripicons-location text-info font-18 mt-2 mr-2"></i> <b>Primary Address</b> : ${address}</li>
						</ul>
						<div class="button-list btn-social-icon">                                                
							<button type="button" class="btn btn-blue btn-round">
								<i class="fab fa-facebook-f"></i>
							</button>

							<button type="button" class="btn btn-secondary btn-round ml-2">
								<i class="fab fa-twitter"></i>
							</button>

							<button type="button" class="btn btn-pink btn-round  ml-2">
								<i class="fab fa-dribbble"></i>
							</button>
						</div>
					</div><!--end col-->
				</div><!--end row-->
			</div><!--end f_profile-->                                                                                
		</div><!--end card-body-->
		<div class="card-body">
			<ul class="nav nav-pills mb-0" id="pills-tab" role="tablist">
				<li class="nav-item">
					<a class="nav-link active" id="general_detail_tab" data-toggle="pill" href="#general_detail">General</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" id="education_detail_tab" data-toggle="pill" href="#education_detail">Education</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" id="portfolio_detail_tab" data-toggle="pill" href="#portfolio_detail">Portfolio</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" id="settings_detail_tab" data-toggle="pill" href="#settings_detail">Settings</a>
				</li>
			</ul>        
		</div><!--end card-body-->
	</div><!--end card-->
</div><!--end col-->
</div>
</body>
`;

frappe.frappe_page = {
	body: body,
}

function changeCurrentTab(newVal) {
	currentTab = newVal;
	render_new_design();
}
// contact tab functions
function getContacts() {
	frappe.call({
		method: "barcode_aec.barcode_aec.page.company_profile.customer_profile.get_contacts_for_customer",
		args: {"customer_name" : docName},
		callback: function(r) {
			contacts = r.message;
			console.log('contacts',contacts);
		},
	});
}
//////////fun. for new contact
function newContactDialog() {
    var modal = document.getElementById('itemDetailsModal');
    var itemDetails = document.getElementById('itemDetails');

	var formHTML = `
            <div class="modal-header">
                <h5 class="modal-title">Add New Contact</h5>
            </div>
            <div class="modal-body">
                <form>
                    <div class="form-group">
                        <label for="first_name">First Name *</label>
                        <input type="text" class="form-control" id="first_name" placeholder="first name" required>
                    </div>
					<div class="form-group">
                        <label for="designation">Designation *</label>
                        <input type="text" class="form-control" id="designation" placeholder="designation" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email address *</label>
                        <input type="email" class="form-control" id="email" placeholder="email" required>
                    </div>
                    <div class="form-group">
                        <label for="phone">Phone Number</label>
                        <input type="text" class="form-control" id="phone" placeholder="phone number">
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal" onClick="closeDialog('itemDetailsModal')">Close</button>
                <button type="button" class="btn btn-primary" onClick="saveContact()">Submit</button>
            </div>`;

    itemDetails.innerHTML = `
        <div>${formHTML}</div>
    `;

    modal.style.display = 'block';

    var closeBtn = document.getElementsByClassName('close')[0];
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };
}
function saveContact() {
    customerId = docName;
    firstName = document.getElementById('first_name').value;
    designation = document.getElementById('designation').value;
    email = document.getElementById('email').value;
    phone = document.getElementById('phone').value ?? "";
	if (!firstName) {
        frappe.msgprint('Please enter a first name');
        return;
    }
    if (!designation) {
        frappe.msgprint('Please enter a designation');
        return;
    }
    if (!email) {
        frappe.msgprint('Please enter an email');
        return;
    }
	if (!isValidEmail(email)) {
        frappe.msgprint('Please enter a valid email address');
        return;
    }

    addNewContact(customerId, firstName, designation, email, phone);
    closeDialog('itemDetailsModal');
	frappe.msgprint('Contact added successfully');
}
function addNewContact(customerId, firstName, designation, email, phone) {
    frappe.call({
        method: "barcode_aec.barcode_aec.page.company_profile.customer_profile.add_contact",
        args: {
            customer_id: customerId,
            first_name: firstName,
			designation: designation,
            email: email,
            phone: phone
        },
        callback: function(response) {
            if (response.message) {
                render_new_design();
            } else {
                frappe.msgprint("Failed to add contact:", response);
            }
        }
    });
}
//////////fun. for close dialog
function closeDialog(dialogId) {
	var modal = document.getElementById(dialogId);
    modal.style.display = 'none';
}
//////////fun. for check email validation
function isValidEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}
//////////fun. for send email
function contactSendEmail(sender) {
    var modal = document.getElementById('emailDialog');
    var itemDetails = document.getElementById('emailFields');

    var formHTML = `
        <div class="modal-header">
            <h5 class="modal-title">Send Email</h5>
        </div>
        <div class="modal-body">
            <form>
                <div class="form-group">
                    <label for="to">To *</label>
					<select class="form-control" id="to" required>
                            <option value="list" disabled selected>Select recipient email</option>
                        </select>
                </div>
				<div class="form-group">
				<label for="to">Sender Email *</label>
				<input type="email" class="form-control" id="sender" placeholder="sender@example.com" value="${sender}" required>
				</div>

                <div class="form-group">
                    <label for="subject">Subject *</label>
                    <input type="text" class="form-control" id="subject" placeholder="Subject" required>
                </div>
                <div class="form-group">
                    <label for="message">Message *</label>
                    <textarea class="form-control" id="message" placeholder="Your message" rows="5" required></textarea>
                </div>
            </form>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" onClick="closeDialog('emailDialog')">Close</button>
            <button type="button" class="btn btn-primary" onClick="sendEmail()">Send</button>
        </div>
    `;

    itemDetails.innerHTML = `
        <div>${formHTML}</div>
    `;

    modal.style.display = 'block';

	var selectElement = document.getElementById('to');
        emails.forEach(function(option) {
            var optionElement = document.createElement("option");
            optionElement.value = option.email_id;
            optionElement.textContent = option.email_id;
            selectElement.appendChild(optionElement);
        });

    var closeBtn = document.getElementsByClassName('close')[0];
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };
}
function sendEmail() {
    var to = document.getElementById('to').value;
	var sender = document.getElementById('sender').value;
    var subject = document.getElementById('subject').value;
    var message = document.getElementById('message').value;

    if (!sender) {
        frappe.msgprint('Please enter a sender email');
        return;
    }
    if (!isValidEmail(sender)) {
        frappe.msgprint('Please enter a valid sender email address');
        return;
    }
	if(!to) {
		frappe.msgprint('Please enter an email');
        return;
	}
	if (!isValidEmail(to)) {
        frappe.msgprint('Please enter a valid email address');
        return;
    }
	if(!subject && !message) {
		frappe.msgprint('Please enter a subject or message');
        return;
	}

    frappe.call({
        method: 'barcode_aec.barcode_aec.page.company_profile.customer_profile.sendmail',
        args: {
            recipients: to,
			sender: sender,
            subject: subject,
            content: message,
            send_email: true
        },
        callback: function(response) {
            if (response.message) {
                frappe.msgprint('mail sent successfully');
            } else {
                frappe.msgprint("Failed to send email");
            }
        }
    });
    closeDialog('emailDialog');
}
////////// Get email to field

    // Function to fetch and populate emails
    function get_emails() {
        console.log("get_emails function called");
        
        frappe.call({
            method: 'barcode_aec.barcode_aec.page.company_profile.customer_profile.get_Email_account',
            callback: function(response) {
                console.log(JSON.stringify(response));
                if (response.message) {
					emails = response.message;
                } else {
                    console.log("Error");
                }
            }
        });
    }


//////////fun. for edit contact
function navigateToContact(contactName) {
    window.location.href = 'http://85.195.99.171/app/contact/' + contactName;
}
//////////fun. for delete contact
function deleteContact(contactId) {
    // frappe.confirm(
    //     'Are you sure you want to delete this contact?', 
    //     function() {
            // This is the "OK" callback function
			if (confirm("Are you sure you want to delete this contact?")) {
				frappe.call({
					method: 'barcode_aec.barcode_aec.page.company_profile.customer_profile.delete_contact',
					args: {
						'doc_name': contactId
					},
					callback: function(r) {
						render_new_design();
					}
				});
			}
			
    //     },
    //     function(){
    //         // This is the "Cancel" callback function
    //         console.log("Deletion cancelled");
    //     }
    // );
}

//////////////////////////////////////////////////////////
// exports tab functions
function fetchExportsData() {
	if(cus.volume_of_member_exports_for_three_years.length > 0){
		dashboardListCurr = cus.volume_of_member_exports_for_three_years;
		const currentYear = new Date().getFullYear();
		const currentSeason = `${currentYear - 1}-${currentYear}`;
		seasonName = dashboardListCurr.reduce((acc, curr) => {
			return acc.season_name < curr.season_name && curr.season_name === currentSeason ? curr : acc;
		});
		const originalSeasonName = { ...seasonName };
		dashboardListCurr = dashboardListCurr.filter(item => item.season_name !== currentSeason);
		lastSeason = dashboardListCurr.reduce((acc, curr) => {
			if(acc.season_name < curr.season_name && curr.season_name < currentSeason) {
				return curr;
			}else{
				return acc;
			}
		});
		seasonName = originalSeasonName;
		if(currentSeason == seasonName.season_name) {
			currSeason = seasonName;
		}else {
			currSeason.total_amount_in_egp = 0;
			currSeason.total_amount_in_usd = 0;
			currSeason.quantity_in_tons = 0;
			currSeason.season_name = currentSeason;
		}
		if(lastSeason.season_name == currentSeason) {
			lastSeason.season_name = 'none';
			lastSeason.total_amount_in_egp = 0;
			lastSeason.total_amount_in_usd = 0;
			lastSeason.quantity_in_tons = 0;
		}
		currSeason.quantity_in_tons = Number(currSeason.quantity_in_tons).toLocaleString();
		currSeason.total_amount_in_egp = Number(currSeason.total_amount_in_egp).toLocaleString();
		currSeason.total_amount_in_usd = Number(currSeason.total_amount_in_usd).toLocaleString();
		lastSeason.quantity_in_tons = Number(lastSeason.quantity_in_tons).toLocaleString();
		lastSeason.total_amount_in_egp = Number(lastSeason.total_amount_in_egp).toLocaleString();
		lastSeason.total_amount_in_usd = Number(lastSeason.total_amount_in_usd).toLocaleString();
	}else {
		const currentYear = new Date().getFullYear();
		const currentSeason = `${currentYear - 1}-${currentYear}`;
		currSeason.season_name = currentSeason;
		currSeason.quantity_in_tons = 0;
		currSeason.total_amount_in_egp = 0;
		currSeason.total_amount_in_usd = 0;
		lastSeason.season_name = 'none';
		lastSeason.quantity_in_tons = 0;
		lastSeason.total_amount_in_egp = 0;
		lastSeason.total_amount_in_usd = 0;
	}
}
//////////////////////////////////////////////////////////
// products tab functions
async function calculateProductsCards() {
	if(cus.custom_crops_that_are_exported.length > 0) {
		let allProducts = cus.custom_crops_that_are_exported;
		let committees = [];
		let products = [];					

		let uniqueValuesCommittees = new Set(allProducts.map(item => item.committees));
    	let uniqueValuesProducts = new Set(allProducts.map(item => item.product));

		committees = Array.from(uniqueValuesCommittees);
    	products = Array.from(uniqueValuesProducts);

		totalCommittees = committees.length;
		totalProducts = products.length;
	}
	if(cus.custom_blocs_of_targeted_countries.length > 0) {
		let allClusters = cus.custom_blocs_of_targeted_countries;
		let clusters = [];

		let uniqueValuesClusters = new Set(allClusters.map(item => item.countries__name));

		clusters = Array.from(uniqueValuesClusters);

		totalClusters = clusters.length;

		frappe.call({
			method: 'barcode_aec.barcode_aec.page.company_profile.customer_profile.get_total_clusters',
			args: {
				'clusters': clusters,
			},
			callback: function(r) {
				totalCountries = r.message.length;
			}
		});
	}
}
function fetchAllProductsDetails() {
	var productss = cus.custom_crops_that_are_exported;
	for(var prod of productss) {
		frappe.call({
			method: "barcode_aec.barcode_aec.page.company_profile.customer_profile.get_product_details",
            args: { "product": prod.product },
			callback: function(r) {
				productsDetails.push(r.message);
				hs_code = r.message.hs_code;
				custom_international_product_hs_code = r.message.custom_international_product_hs_code;
				scientific_arabic_name = r.message.scientific_arabic_name;
				scientific_english_name = r.message.scientific_english_name;
			}
		});
	}
}
function openItemDetailsModal(name, images, productCommittee, code, englishName) {
    var modal = document.getElementById('itemDetailsModal');
    var itemDetails = document.getElementById('itemDetails');
	var imageList = images.split(',');

	var imageSliderHTML = '';
	if(imageList.length > 0) {
		imageSliderHTML = `<div id="image-slider" class="splide">
  								<div class="splide__track">
									<ul class="splide__list">`;
		for (var i = 0; i < imageList.length; i++) {
			imageSliderHTML += `		<li class="splide__slide">
											<img src="${imageList[i]}">
										</li>`;
		}
		imageSliderHTML += `		</ul>
  								</div>
							</div>`;
	}else {
		imageSliderHTML = `<img src="https://eu.ui-avatars.com/api/?name=${name}&size=250" alt="avatar" class="rounded-circle">`;
	}

    itemDetails.innerHTML = `
	<div class="row">
        <div class="slider-container">${imageSliderHTML}</div>
        <div class="details">
            <h3>${name}</h3>
            <p><strong>English Name:</strong> ${englishName}</p>
            <p><strong>(HS Code) Local Product Code:</strong> ${code}</p>
            <p><strong>Product Committee:</strong> ${productCommittee}</p>
        </div>
	</div>
    `;

    modal.style.display = 'block';

    var closeBtn = document.getElementsByClassName('close')[0];
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

	new Splide( '#image-slider', {
        type: 'slide',
        rewind: false,
        width: '100%',
        heightRatio: 0.5,
        perPage: 1,
        pagination: true,
        focus: 'center',
    } ).mount();
}
//////////////////////////////////////////////////////////
// check current customer
function currentCustomer() {
	if(!frappe.get_route()[1].includes('ustomer')) {
		if(docName != frappe.get_route()[1]) {
			fetchData();
		}
	}else {
		frappe.ui.toolbar.clear_cache();
	}
}

function render_new_design() {
	setInterval(currentCustomer, 500);
// html head with styles
let nBody = `
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@splidejs/splide@3.0.9/dist/css/splide.min.css">
<script src="https://cdn.jsdelivr.net/npm/@splidejs/splide@3.0.9/dist/js/splide.min.js"></script>
<link href='https://fonts.googleapis.com/css?family=Cairo' rel='stylesheet'>
<link rel="stylesheet" href="https://unpkg.com/@icon/dripicons/dripicons.css">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
<style>
.splide__slide img {
  width: 100%;
  height: auto;
}
.splide__pagination {
    bottom: 10px;
}

.splide__pagination__page {
    background-color: #006738;
}

.splide__pagination__page.is-active {
    background-color: #ff0000;
}

.slider-container {
    display: flex;
    flex-wrap: nowrap;
    overflow-x: auto;
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE and Edge */
}

.slider-container::-webkit-scrollbar {
    display: none; /* Chrome, Safari, Opera */
}

.slider-image {
    flex: 0 0 auto;
    margin-right: 10px;
}

.details {
    padding: 10px;
}

.modal {
    display: none;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
}

.close:hover,
.close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
}


.container1 {
    border-radius: 3px;
    overflow: hidden;
    label {
      display: inline-block;
      font-size: 16px;
      line-height: 36px;
      text-align: center;
      color: #555;
	  padding-bottom: 10px;
      transition: background 0.25s ease;
      cursor: pointer;
      &:hover::after {
        opacity: 1;
      }
    }
    .line {
      height: 2px;
      background: #B2BEB5;
      width: 100%;
      top: 34px;
      left: 0;
      transition: left 0.25s ease;
    }
  }
  body {
    font-family: 'Cairo';
}
.text-body {
	border: 2px solid black; 
	border-radius: 3px; 
	padding: 5px;
}

.btn-soft-secondary {
	background-color: rgba(255, 0, 0, 0.5);
	color: #ffffff;
}
  
.btn-soft-secondary:hover {
	background-color: rgba(255, 0, 0, 1);
	color: #ffffff;
}
  
.btn-soft-secondary:focus {
	-webkit-box-shadow: 0 0 0 0.1rem rgba(255, 0, 0, 0.3);
			box-shadow: 0 0 0 0.1rem rgba(255, 0, 0, 0.3);
	background-color: rgba(255, 0, 0, 0.8);
	color: #ffffff;
}

.btn-soft-primary {
	background-color: rgba(77, 121, 246, 0.1);
	color: #4d79f6;
}
  
.btn-soft-primary:hover {
	background-color: #4d79f6;
	color: #ffffff;
}
  
.btn-soft-primary:focus {
	-webkit-box-shadow: 0 0 0 0.1rem rgba(77, 121, 246, 0.2);
			box-shadow: 0 0 0 0.1rem rgba(77, 121, 246, 0.2);
	background-color: rgba(77, 121, 246, 0.8);
	color: #ffffff;
}

.thumb-xl {
	height: 78px;
	width: 78px;
	font-size: 28px;
	font-weight: 700;
}

.met-profile .met-profile-main {
	display: -webkit-box;
	display: -ms-flexbox;
	display: flex;
	-webkit-box-orient: horizontal;
	-webkit-box-direction: normal;
		-ms-flex-direction: row;
			flex-direction: row;
	-webkit-box-flex: 1;
		-ms-flex: 1;
			flex: 1;
	-ms-flex-wrap: wrap;
		flex-wrap: wrap;
	-webkit-box-align: center;
		-ms-flex-align: center;
			align-items: center;
}

.met-profile .met-profile-main .met-profile-main-pic {
	position: relative;
	max-width: 128px;
	max-height: 128px;
	margin-right: 24px;
}

.met-profile .met-profile-main .met-profile-main-pic .fro-profile_main-pic-change {
	cursor: pointer;
	background-color: #4d79f6;
	border-radius: 50%;
	width: 32px;
	height: 32px;
	position: absolute;
	bottom: 4px;
	right: 4px;
	display: -webkit-box;
	display: -ms-flexbox;
	display: flex;
	-webkit-box-align: center;
		-ms-flex-align: center;
			align-items: center;
	-webkit-box-pack: center;
		-ms-flex-pack: center;
			justify-content: center;
	-webkit-box-flex: 1;
		-ms-flex: 1;
			flex: 1;
	-webkit-box-shadow: 0px 0px 20px 0px rgba(32, 41, 74, 0.05);
			box-shadow: 0px 0px 20px 0px rgba(32, 41, 74, 0.05);
	/* Apply the animation */
	animation: shine 1s infinite;
}

.met-profile .met-profile-main .met-profile-main-pic .fro-profile_main-pic-change i {
	-webkit-transition: all 0.3s;
	transition: all 0.3s;
	color: #ffffff;
	font-size: 16px;
}

.met-profile .met-profile-main .met-profile_user-detail .met-user-name {
	font-size: 15px;
	font-weight: 600;
	color: #ffffff;
	margin-bottom: 6px;
}

.met-profile .met-profile-main .met-profile_user-detail .met-user-name-post {
	color: #ffffff;
}

.met-profile .personal-detail li {
	color: #aeb4ce;
}

.rounded-circle {
	border-radius: 50%;
    overflow: hidden;
    width: 128px;
    height: 128px;
	border: 2px solid #fff;
}

.nav-item a.nav-link{
	background-color: #ADD8E6;
	color: #000000;
	margin: 5px;
}

.nav-item a.nav-link.active {
	background-color: #ADD8E6;
	color: #008080;
	margin: 5px;
}

.met-profile .personal-detail li.desc {
	color: #ffffff;
}

.own-detail {
	padding: 20px;
	width: 145px;
	height: 145px;
	text-align: center;
	border-radius: 52% 48% 23% 77% / 44% 68% 32% 56%;
	-webkit-box-shadow: 0px 0px 3px 1.25px #50649c;
			box-shadow: 0px 0px 3px 1.25px #50649c;
}
  
.own-detail h1 {
	font-weight: 600;
	color: #ffffff;
	margin-top: 0;
}
  
.own-detail h5 {
	color: #f2f2f2;
}
  
.own-detail.own-detail-project {
	position: absolute;
	top: 110px;
	left: -60px;
}
  
.own-detail.own-detail-happy {
	position: absolute;
	top: 110px;
	left: 60px;
}
  
@media (max-width: 767px) {
	.own-detail {
	  display: none;
}

.bg-blue {
	background-color: #2b55cc !important;
}

.bg-secondary {
  background-color: #4ac7ec !important;
}

.bg-success {
	background-color: #1ecab8 !important;
}

.page-content {
	width: 100%;
	position: relative;
	min-height: calc(100vh - 70px);
	padding: 0 10px 60px 10px;
}

@media (max-width: 1024px) {
	.left-sidenav {
	  position: fixed;
	  top: 70px;
	  overflow-y: auto;
	  z-index: 5;
	  bottom: 0;
	}
	.page-content {
	  min-height: 100vh;
	}
	.enlarge-menu .topbar .topbar-left {
	  margin-left: 0;
	  width: 70px;
	}
}

@media print {
	.logo, .page-title, .breadcrumb, .footer {
	  display: none;
	  margin: 0;
	  padding: 0;
	}
	.left {
	  display: none;
	}
	.content, .page-content-wrapper, .page-wrapper {
	  margin-top: 0;
	  padding-top: 0;
	}
	.content-page {
	  margin-left: 0;
	  margin-top: 0;
	}
	.topbar, .footer, .left-sidenav, .report-btn {
	  display: none;
	  margin: 0;
	  padding: 0;
	}
	.content-page > .content {
	  margin: 0;
	}
}

.container-fluid {
	padding-right: 12px;
	padding-left: 12px;
}

.dataTables_wrapper.container-fluid {
	padding: 0;
}

@media (min-width: 680px) {
	.page-wrapper {
	  display: -webkit-box;
	  display: -ms-flexbox;
	  display: flex;
	}
}

.page-wrapper {
	padding-top: 70px;
}

@keyframes shine {
	to {
		background-position-x: -200%;
	}
}
#phoneicon2 {
    color: red !important;
}

</style>

</head>
`;
// personal info bar
nBody += `
<body>
<div class="page-wrapper">
	<div class="page-content">
		<div class="container-fluid">
			<div class="row">
				<div class="col-12">
					<div class="card">
						<div class="card-body  met-pro-bg" style="background-image: url('/files/background.jpeg'); border-radius: 15px 15px 0px 0px;">
							<div class="met-profile shine">
								<div class="row">
									<div class="col-lg-8 align-self-center mb-3 mb-lg-0">
										<div class="met-profile-main">
											<div class="met-profile-main-pic">`;
nBody+=											badge;
nBody+=`										
											</div>
											<div class="met-profile_user-detail">
												<h5 class="met-user-name" style="color: black;">${customer_name}</h5> 
											</div>
										</div>                                                
									</div><!--end col-->
									<div class="col-lg-4 ml-auto">
										<ul class="list-unstyled personal-detail">
											<li class="desc" style="color: black;"><i id = "phoneicon2"; class="dripicons dripicons-phone mr-2 text-info font-18" style="color: #006738 !important;"></i><b> Company Mobile </b> : ${mobile}</li>
											<li class="desc mt-2" style="color: black;"><i class="dripicons dripicons-mail text-info font-18 mt-2 mr-2" style="color: #006738 !important;"></i> <b> Company Email </b> : ${email}</li>
											<li class="desc mt-2" style="color: black;"><i class="dripicons dripicons-location text-info font-18 mt-2 mr-2" style="color: #006738 !important;"></i> <b>Primary Address</b> : ${address}</li>
										</ul>
									</div><!--end col-->
								</div><!--end row-->
							</div><!--end f_profile-->                                                                                
						</div><!--end card-body-->
						`;
if(currentTab == 'details') {
	nBody+=`
						<div class="card-body">
							<div class="container1">
								<label style=" margin-right: 15px; padding: 5px; color: #006738; border-bottom: 2px solid #006738;" onclick="changeCurrentTab('details')">Details</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('committees')">Committees</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('contact')">Contacts</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('exports')">Exports</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('items')">Products</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('requests')">Requests</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('services')">E-service</label>
							</div>      
						</div><!--end card-body-->
					</div><!--end card-->
				</div><!--end col-->
			</div><!--end row and end of top part--> 
			<div class="row">
				<div class="col-12">
					<div class="tab-content detail-list" id="pills-tabContent">
						<div class="tab-pane fade show active" id="general">
                            <div class="row">
                            	<div class="col-12">
                                    <div class="card">
                                        <div class="card-body">
										
                                            	<div class="row" >

												
												<div class="col-lg-2">`;

nBody +=companyOwnerPic !== '' ?  					`<img src="${companyOwnerPic}" alt="profile photo">`  :	`<img src="/files/placeholder.png" alt="profile photo">`;
nBody+=`										</div>
                                                <div class="col-lg-6">
													<div style="font-size: 20px;">${cus.custom_name_of_the_cioowner_of_the_company}</div>
													<br>
													<div style="font-size: 15px;">Address: ${cus.primary_address}</div>
													<div style="font-size: 15px;">Governorate: ${cus.territory}</div>
													<div style="font-size: 15px;">Joining Date: ${cus.custom_joining_date}</div>
													<div style="font-size: 15px;">Representative: ${cus.custom_responsible_persons_name}</div>
													
													
													<br>`;
nBody += customerStatus =="Active"?`				<div><p class="mb-0 met-user-name-post" style=" font-size:24px; font-weight: 900; color: green;">${customerStatus}</p></div>` 
												  :`<div><p class="mb-0 met-user-name-post" style="color: red;">${customerStatus}</p></div>`;
	  nBody+= customerStatus =="Suspended"? 	   `<div><p class="mb-0 met-user-name-post">Reason: <span style="color: red;">${reason}</span></p></div>` : `<div></div>`;



	  nBody+=`                              	</div>`;
	///////////////////////////////////////////////////////////////////////////////////
if(blocs.length > 0) {
		nBody+=	`<div class="col-lg-12"  style="display: flex; justify-content: center;"" ><table class="table table-bordered dt-reponsive nowrap" style=" align-content: center; border: 0.2px solid #019879; width: 90%; text-align: center; border-radius: 30px; border-collapse: seperate;">
	<thead style="color: #ffffff;">
		<tr>
			<th style="width: 50%; border-radius: 30px 0 0 0; background-color: #006738;">Countries</th>
			<th style="width: 50%; border-radius: 0 30px 0 0; background-color: #006738;">Clusters </th>
		</tr>
	</thead>
	<tbody>	`;
	for(var bloc of blocs) {
		nBody+=	`
						<tr>
						<td style="border: 0.5px solid #006738; width: 50%;">${bloc.country_name}</td>
						<td style="border: 0.5px solid #006738; width: 50%;">${bloc.cluster_name}</td>
						</tr>`;		
	}

	nBody+=	`		</tbody>
	</table></div>`;
	}
///////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////
											
											
												
										
										  
        nBody+=`                                    </div>
                                        </div><!--end card-body-->
                                    </div><!--end card-->
                                </div><!--end col-->
                            </div><!--end row-->                                             
                        </div><!--end general detail-->
					</div><!--end tabs pages-->
				</div>
			</div>
		</div>
	</div>
</div>
</body>
`;
}else if(currentTab == 'committees') {
	nBody+=`
						<div class="card-body">
							<div class="container1">
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('details')">Details</label>
								<label style=" margin-right: 15px; padding: 5px; color: #006738; border-bottom: 2px solid #006738;" onclick="changeCurrentTab('committees')">Committees</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('contact')">Contacts</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('exports')">Exports</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('items')">Products</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('requests')">Requests</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('services')">E-service</label>
							</div>   
						</div><!--end card-body-->
					</div><!--end card-->
				</div><!--end col-->
			</div><!--end row--> 
			<div class="row">
				<div class="col-12">
					<div class="tab-content detail-list" id="pills-tabContent">
						<div class="tab-pane fade show active" id="data">
                            <div class="row">
                            	<div class="col-12">                                            
                                    <div class="card">
                                        <div class="card-body">
                                            <div class="row" style="justify-content: center;">
												<div style="text-align: center; width: 100%;"><h3>اللجان</h3></div>
                                                <table class="table table-bordered dt-reponsive nowrap" style="border: 0.2px solid #019879; width: 90%; text-align: center; border-radius: 30px; border-collapse: seperate;">
													<thead style="color: #ffffff;">
														<tr>
															<th style="width: 50%; border-radius: 30px 0 0 0; background-color: #006738;">Committee</th>
															<th style="width: 50%; border-radius: 0 30px 0 0; background-color: #006738;">نوع العضوية</th>
														</tr>
													</thead>
													<tbody>`;
								for(var row of cus.custom_committees_you_would_like_to_join){
									nBody+=	`			<tr>
															<td style="border: 0.5px solid #006738; width: 50%;">${row.committees}</td>
															<td style="border: 0.5px solid #006738; width: 50%;">${row.salutation}</td>
														</tr>`;
								}
									nBody+=	`		</tbody>
												</table>`;
			///add stations and farm tables
			if(cus.custom_does_the_company_have_a_filling_station == "Yes") {
				if(cus.custom_packaging_station_details.length > 0 || cus.custom_farm_packing_products.length > 0) {
					nBody += `  <div style="text-align: center; width: 100%;"><h3>محطات التعبئة</h3></div>`;
				}
				if(cus.custom_packaging_station_details.length > 0) {
			nBody += `		<table class="table table-bordered dt-reponsive nowrap" style="border: 0.2px solid #019879; width: 90%; text-align: center; border-radius: 30px; border-collapse: seperate;">
								<thead style="color: #ffffff;">
									<tr>
										<th style="width: 50%; border-radius: 30px 0 0 0; background-color: #006738;">Station Name</th>
										<th style="width: 50%; border-radius: 0 30px 0 0; background-color: #006738;">Station Address</th>
									</tr>
								</thead>
								<tbody>`;
					for(var row of cus.custom_packaging_station_details) {
						nBody+=	`	<tr>
										<td style="border: 0.5px solid #006738; width: 50%;">${row.station_name}</td>
										<td style="border: 0.5px solid #006738; width: 50%;">${row.station_address}</td>
									</tr>`;
					}
					nBody+=	`	</tbody>
							</table>`;
				}
				if(cus.custom_farm_packing_products.length > 0) {
					nBody += `<table class="table table-bordered dt-reponsive nowrap" style="border: 0.2px solid #019879; width: 90%; text-align: center; border-radius: 30px; border-collapse: seperate;">
								<thead style="color: #ffffff;">
									<tr>
										<th style="width: 50%; border-radius: 30px 0 0 0; background-color: #006738;">Committee</th>
										<th style="width: 50%; border-radius: 0 30px 0 0; background-color: #006738;">Product</th>
									</tr>
								</thead>
								<tbody>`;
					for(var row of cus.custom_farm_packing_products) {
						nBody+=	`	<tr>
										<td style="border: 0.5px solid #006738; width: 50%;">${row.committee}</td>
										<td style="border: 0.5px solid #006738; width: 50%;">${row.item}</td>
									</tr>`;
					}
					nBody+=	`	</tbody>
							</table>`;
				}
			}
			if(cus.custom_does_the_company_own_a_farm == "Yes") {
				if(cus.custom_crops_that_the_company_packs_at_the_station.length > 0 || cus.custom_members_farm_details_.length > 0) {
					nBody += `	<div style="text-align: center; width: 100%;"><h3>بيانات المزارع</h3></div>`;
				}
				if(cus.custom_crops_that_the_company_packs_at_the_station.length > 0) {
			nBody += `		<table class="table table-bordered dt-reponsive nowrap" style="border: 0.2px solid #019879; width: 90%; text-align: center; border-radius: 30px; border-collapse: seperate;">
								<thead style="color: #ffffff;">
									<tr>
										<th style="width: 50%; border-radius: 30px 0 0 0; background-color: #006738;">Comittee</th>
										<th style="width: 50%; border-radius: 0 30px 0 0; background-color: #006738;">Product</th>
									</tr>
								</thead>
								<tbody>`;
					for(var row of cus.custom_crops_that_the_company_packs_at_the_station) {
						nBody+=	`	<tr>
										<td style="border: 0.5px solid #006738; width: 50%;">${row.committee}</td>
										<td style="border: 0.5px solid #006738; width: 50%;">${row.item}</td>
									</tr>`;
					}
					nBody+=	`	</tbody>
							</table>`;
				}
				if(cus.custom_members_farm_details_.length > 0) {
					nBody += `<table class="table table-bordered dt-reponsive nowrap" style="border: 0.2px solid #019879; width: 90%; text-align: center; border-radius: 30px; border-collapse: seperate;">
								<thead style="color: #ffffff;">
									<tr>
										<th style="width: 50%; border-radius: 30px 0 0 0; background-color: #006738;">Committee</th>
										<th style="width: 50%; border-radius: 0 30px 0 0; background-color: #006738;">Product</th>
									</tr>
								</thead>
								<tbody>`;
					for(var row of cus.custom_members_farm_details_) {
						nBody+=	`	<tr>
										<td style="border: 0.5px solid #006738; width: 50%;">${row.farm_name}</td>
										<td style="border: 0.5px solid #006738; width: 50%;">${row.farm_address}</td>
									</tr>`;
					}
					nBody+=	`	</tbody>
							</table>`;
				}
			}
                                nBody+=`    </div>         
                                        </div><!--end card-body-->
                                    </div><!--end card-->
                                </div><!--end col-->
                            </div><!--end row-->                                             
                        </div><!--end general detail-->
					</div><!--end tabs pages-->
				</div>
			</div>
		</div>
	</div>
</div>
</body>
`;
}else if(currentTab == 'contact') {
	getContacts();
	nBody+=`
						<div class="card-body">
							<div class="container1">
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('details')">Details</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('committees')">Committees</label>
								<label style=" margin-right: 15px; padding: 5px; color: #006738; border-bottom: 2px solid #006738;" onclick="changeCurrentTab('contact')">Contacts</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('exports')">Exports</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('items')">Products</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('requests')">Requests</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('services')">E-service</label>
							</div>         
						</div><!--end card-body-->
					</div><!--end card-->
				</div><!--end col-->
			</div><!--end row--> 
			<div class="row">
				<div class="col-12">
					<div class="tab-content detail-list" id="pills-tabContent">
						<div class="tab-pane fade show active" id="data">
                            <div class="row">
                            	<div class="col-12">                                            
                                    <div class="card">
                                        <div class="card-body">
											<div class="row justify-content-end">
												<button class="btn px-4 float-right mt-0 mb-3" id="btnAddContact" style="background-color: #006738; color: white; font-size: 16px;" onclick="newContactDialog()"><i class="far fa-plus fa-lg"></i> Add New Contact</button>
											</div>`;
				nBody+=                	   `<div id="itemDetailsModal" class="modal">
												<div class="modal-content" style="width: 50%; justify-content: center;">
													<span class="close">&times;</span>
													<div id="itemDetails"></div>
												</div>
											</div>`;
				nBody+=                	   `<div id="emailDialog" class="modal">
												<div class="modal-content" style="width: 50%; justify-content: center;">
													<span class="close">&times;</span>
													<div id="emailFields"></div>
												</div>
											</div>`;
                nBody+=                    `<div class="row">`;
						for(var contact of contacts) {
							let designation = contact.designation == null || contact.designation == "" ? "" : contact.designation;
                nBody+=                        `<div class="col-3">
													<div class="card client-card" style="height: 400px">
														<div class="card-body text-center">
															<img src="/files/communication.png" width="75px" height="75px">
															<h5 style="color: black; margin-top: 15px;">${contact.first_name}</h5>`;
							nBody+= designation == "" ?    `<div class="col-12" style="margin-top: 15px; content-justify: center; color: white;">
																<span>.</span>
															</div>` :
														   `<div class="col-12" style="margin-top: 15px; content-justify: center;">
																<span class="text-muted">${designation}</span>
															</div>`;
				nBody+= contact.email_id != "" ?		   `<span class="text-muted"><i class="dripicons dripicons-message mr-2 text-info " style=" color: #006738;" ></i>${contact.email_id}</span><br>` : `<span></span>`;
				nBody+= contact.phone != "" ?			   `<span class="text-muted"><i class="dripicons dripicons-phone mr-2 text-info" style=" color: #006738;" ></i>${contact.phone}</span><br>` : `<span style="color: white;">.</span><br>`;
				nBody+=									   `<div class="col-12" style="margin-top: 15px; content-justify: center;">
																<button type="button" class="btn btn-sm btn-soft-primary" style="background-color: #006738; color: white;" onclick="contactSendEmail('${contact.email_id}')"><i class="far fa-message fa-lg"></i> Message</button>
															</div>
															<div class="col-12" style="margin-top: 15px; content-justify: center;">
																<button type="button" class="btn btn-sm btn-soft-secondary" style="background-color: #006738; color: white;" onclick="navigateToContact('${contact.name}')"><i class="far fa-edit fa-lg"></i> Edit</button>
																<button type="button" class="btn btn-sm btn-soft-secondary" style="background-color: #006738; color: white;" onclick="deleteContact('${contact.name}')"><i class="far fa-trash-alt fa-lg"></i> Delete</button>
															</div>
														</div><!--end card-body-->
													</div><!--end card-->
                                                </div><!--end col-->`
						}
                nBody+=`                 	</div><!--end row-->
                                        </div><!--end card-body-->
                                    </div><!--end card-->
                                </div><!--end col-->
                            </div><!--end row-->                                             
                        </div><!--end general detail-->
					</div><!--end tabs pages-->
				</div>
			</div>
		</div>
	</div>
</div>
</body>
`;
}else if(currentTab == 'exports') {
	nBody+=`
						<div class="card-body">
							<div class="container1">
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('details')">Details</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('committees')">Committees</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('contact')">Contacts</label>
								<label style=" margin-right: 15px; padding: 5px; color: #006738; border-bottom: 2px solid #006738;" onclick="changeCurrentTab('exports')">Exports</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('items')">Products</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('requests')">Requests</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('services')">E-service</label>
							</div>         
						</div><!--end card-body-->
					</div><!--end card-->
				</div><!--end col-->
			</div><!--end row--> 
			<div class="row">
				<div class="col-12">
					<div class="tab-content detail-list" id="pills-tabContent">
						<div class="tab-pane fade show active" id="data">
                            <div class="row">
                            	<div class="col-12">                                            
                                    <div class="card">
                                        <div class="card-body">
											<div class="row justify-content-center">
												<div class="col-md-3">
													<div class="card report-card">
														<div class="card-body">
															<span class="badge badge-success" style = "align-content: center; font-size: 15px;	width:75px; height:18px;">${currSeason.season_name}</span>
															<h3 class="my-3">${currSeason.quantity_in_tons} Ton</h3>
															<p class="mb-0 text-muted text-truncate">حجم الصادرات بالطن</p>
														</div><!--end card-body--> 
													</div><!--end card--> 
												</div> <!--end col-->
												<div class="col-md-3">
													<div class="card report-card">
														<div class="card-body">
															<span class="badge badge-success"  style = "align-content: center; font-size: 15px;	width:75px; height:18px;">${currSeason.season_name}</span>
															<h3 class="my-3">${currSeason.total_amount_in_egp} EGP</h3>
															<p class="mb-0 text-muted text-truncate">حجم الصادرات بالجنيه المصري</p>
														</div><!--end card-body--> 
													</div><!--end card--> 
												</div> <!--end col-->
												<div class="col-md-3">
													<div class="card report-card">
														<div class="card-body">
															<span class="badge badge-success" style = "align-content: center; font-size: 15px;	width:75px; height:18px;">${currSeason.season_name}</span>
															<h3 class="my-3">${currSeason.total_amount_in_usd} USD</h3>
															<p class="mb-0 text-muted text-truncate">حجم الصادرات بالدولار</p>
														</div><!--end card-body--> 
													</div><!--end card--> 
												</div> <!--end col-->
												<div class="col-md-3">
													<div class="card report-card">
														<div class="card-body">
															<span class="badge badge-success" style = " align-content: center; font-size: 15px;	width:75px; height:18px; background-color: #09147d;">${lastSeason.season_name}</span>
															<h3 class="my-3">${lastSeason.quantity_in_tons} Ton</h3>
															<p class="mb-0 text-muted text-truncate">حجم الصادرات بالطن</p>
														</div><!--end card-body--> 
													</div><!--end card--> 
												</div> <!--end col-->
												
													<div class="col-3">
														<div id="dashboardChartTon"></div>
													</div><!--end col-->
													<div class="col-3">
														<div id="dashboardChartDollar"></div>
													</div><!--end col-->
													<!--end col-->
													<div class="col-3">
														<div id="dashboardChartEgp"></div>
													</div>

												<div class="col-md-3">
													<div class="card report-card" style= "margin-top: 15px;">
														<div class="card-body">
															<span class="badge badge-success" style = "align-content: center; font-size: 15px;	width:75px; height:18px; background-color: #09147d;" >${lastSeason.season_name}</span>
															<h3 class="my-3" >${lastSeason.total_amount_in_egp} EGP</h3>
															<p class="mb-0 text-muted text-truncate">حجم الصادرات بالجنيه المصري</p>
														</div><!--end card-body--> 
													</div><!--end card--> 
												</div> <!--end col-->
												<div class="col-9">
													<div id="dashboardChart"></div>
                                                </div><!--end col-->`;
nBody+=cus.volume_of_member_exports_for_three_years.length > 0? `<div class="col-md-3" style="margin-top: -100px">
													<div class="card report-card" style = "margin-top: 25px;">
														<div class="card-body" >
															<span class="badge badge-success" style = "align-content: center; font-size: 15px;	width:75px; height:18px; background-color: #09147d;" >${lastSeason.season_name}</span>
															<h3 class="my-3">${lastSeason.total_amount_in_usd} USD</h3>
															<p class="mb-0 text-muted text-truncate">حجم الصادرات بالدولار</p>
														</div><!--end card-body--> 
													</div><!--end card--> 
												</div> <!--end col-->`
											  :`<div class="col-md-3">
											  		<div class="card report-card" style = "margin-top: 15px;">
												  		<div class="card-body">
													  		<span class="badge badge-success" style = "align-content: center; font-size: 15px;	width:75px; height:18px; background-color: #09147d;" >${lastSeason.season_name}</span>
													  		<h3 class="my-3">${lastSeason.total_amount_in_usd} USD</h3>
													  		<p class="mb-0 text-muted text-truncate">2222حجم الصادرات بالدولار</p>
												  		</div><!--end card-body--> 
											  		</div><!--end card--> 
										  		</div> <!--end col-->`;
			nBody+=		    				`</div>
                                        </div><!--end card-body-->
                                    </div><!--end card-->
                                </div><!--end col-->
                            </div><!--end row-->                                             
                        </div><!--end general detail-->
					</div><!--end tabs pages-->
				</div>
			</div>
		</div>
	</div>
</div>
</body>
`;
}else if(currentTab == 'items') {
	calculateProductsCards();
	nBody+=`
						<div class="card-body">
							<div class="container1">
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('details')">Details</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('committees')">Committees</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('contact')">Contacts</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('exports')">Exports</label>
								<label style=" margin-right: 15px; padding: 5px; 5px; color: #006738; border-bottom: 2px solid #006738;" onclick="changeCurrentTab('items')">Products</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('requests')">Requests</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('services')">E-service</label>
							</div>         
						</div><!--end card-body-->
					</div><!--end card-->
				</div><!--end col-->
			</div><!--end row--> 
			<div class="row">
				<div class="col-12">
					<div class="tab-content detail-list" id="pills-tabContent">
						<div class="tab-pane fade show active" id="data">
                            <div class="row">
                            	<div class="col-12">                                            
                                    <div class="card">
                                        <div class="card-body">
											<div class="row">
												<hr>
												<div class="card report-card col-2">
													<div class="card-body">
														<h3 class="my-3">${totalCommittees}</h3>
														<p style="color: #006738;"><b>Total Committees</b></p>
													</div><!--end card-body--> 
												</div><!--end card--> 
												<hr>
												<div class="card report-card col-2">
													<div class="card-body">
														<h3 class="my-3">${totalProducts}</h3>
														<p style="color: #006738;"><b>Total Products</b></p>
													</div><!--end card-body--> 
												</div><!--end card--> 
												<hr>
												<div class="card report-card col-2">
													<div class="card-body">
														<h3 class="my-3">${totalCountries}</h3>
														<p style="color: #006738;"><b>Total Countries</b></p>
													</div><!--end card-body--> 
												</div><!--end card--> 
												<hr>
												<div class="card report-card col-2">
													<div class="card-body">
														<h3 class="my-3">${totalClusters}</h3>
														<p style="color: #006738;"><b>Total Clusters</b></p>
													</div><!--end card-body--> 
												</div><!--end card--> 
												<hr>
											</div>`;
					nBody+=                `<div id="itemDetailsModal" class="modal">
												<div class="modal-content" style="width: 50%; justify-content: center;">
													<span class="close">&times;</span>
													<div id="itemDetails"></div>
												</div>
											</div>
											`;
                    nBody+=                `<div class="row">
												<div class="col-1"></div>
                                                <div class="col-10">`;
			if(cus.custom_crops_that_are_exported.length > 0) {
							nBody+=				   `<table class="table table-bordered dt-reponsive nowrap" style="border: 0.2px solid #019879; width: 100%; text-align: center; border-radius: 30px; border-collapse: seperate;">
														<thead>
															<tr>
																<th style="border-radius: 30px 0 0 0; background-color: #006738; color: #ffffff;">Image</th>
																<th style="background-color: #006738; color: #ffffff;">Product Name</th>
																<th style="background-color: #006738; color: #ffffff;">Local Product Code</th>
																<th style="background-color: #006738; color: #ffffff;">HS Code family</th>
																<th style="background-color: #006738; color: #ffffff;">InternationalProduct HS Code</th>
																<th style="background-color: #006738; color: #ffffff;">Arabic Name</th>
																<th style="background-color: #006738; color: #ffffff;">English Name</th>
																<th style="background-color: #006738; color: #ffffff;">Scientific Arabic Name</th>
																<th style="background-color: #006738; color: #ffffff;">Scientific English Name</th>
																<th style="background-color: #006738; color: #ffffff;">Committee</th>
																<th style="border-radius: 0 30px 0 0; background-color: #006738; color: #ffffff;">Action</th>
															</tr>
														</thead>
														<tbody>`;
    for (var row of productsDetails) {
		let product_images = [];
		let Names = row.product_common_name;

		for(var name of Names) {
			arabic_name = name.arabic_name;
			english_name = name.english_name;

		}

		for(var imagee of row.products_image) {
			product_images.push(imagee.attach);
		}
        let image = '';
        image = row.product_image ? `<img src="${row.product_image}" alt="avatar" width="200px" height="200px">` :
            `<img src="https://eu.ui-avatars.com/api/?name=${row.scientific_arabic_name}&size=250" alt="avatar" class="rounded-circle">`;
        nBody += 										   `<tr>
            													<td>${image}</td>
            													<td style="padding: 5px; cursor: pointer;" onclick="openItemDetailsModal('${row.scientific_arabic_name}', '${product_images.toString()}', '${row.committe_code}', '${row.name}', '${row.scientific_english_name}')">${row.scientific_arabic_name}</td>
            													<td>${row.name}</td>
																<td>${hs_code}</td>
																<td>${custom_international_product_hs_code}</td>
																<td>${arabic_name}</td>
																<td>${english_name}</td>
																<td>${scientific_arabic_name}</td>
																<td>${scientific_english_name}</td>
																`;
		nBody +=`												<td>${row.committe_code}</td>
            													<td>
                													<a href=""><i class="fas fa-edit text-info mr-1" style="color: #006738 !important;"></i></a>
            													</td>
        													</tr>`;
    }
						nBody+=`						</tbody>
                                    				</table> `;
			}
			if(cus.custom_blocs_of_targeted_countries.length > 0) {
						nBody+=`					<table class="table table-bordered dt-reponsive nowrap" style="border: 0.2px solid #019879; width: 100%; text-align: center; border-radius: 30px; border-collapse: seperate;">
														<thead>
															<tr>
															<th style="border-radius: 30px 0 0 0; background-color: #006738; color: #ffffff;">Geoghrafical Clusters Name</th>
														
														
															<th style="border-radius: 0 30px 0 0; background-color: #006738; color: #ffffff;">Countries Name</th>
															
															</tr>
														</thead>
														<tbody>
						`;			
					for(var row of cus.custom_blocs_of_targeted_countries) {
						nBody+=`							<tr>
														
																<td>${row.cluster_name}</td>
																<td>${row.country_name}</td>
                                        					</tr>`;
					}
						nBody+=`						</tbody>
                                    				</table> `;		
			}		
                        nBody+=`                </div><!--end col-->
                                            </div><!--end row-->
                                        </div><!--end card-body-->
                                    </div><!--end card-->
                                </div><!--end col-->
                            </div><!--end row-->                                             
                        </div><!--end general detail-->
					</div><!--end tabs pages-->
				</div>
			</div>
		</div>
	</div>
</div>
</body>
`;
}else if(currentTab == 'requests') {
	nBody+=`
						<div class="card-body">
							<div class="container1">
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('details')">Details</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('committees')">Committees</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('contact')">Contacts</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('exports')">Exports</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('items')">Products</label>
								<label style=" margin-right: 15px; padding: 5px; color: #006738; border-bottom: 2px solid #006738;" onclick="changeCurrentTab('requests')">Requests</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('services')">E-service</label>
							</div>      
						</div><!--end card-body-->
					</div><!--end card-->
				</div><!--end col-->
			</div><!--end row and end of top part--> 
			<div class="row">
				<div class="col-12">
					<div class="tab-content detail-list" id="pills-tabContent">
						<div class="tab-pane fade show active" id="general">
                            <div class="row">
                            	<div class="col-12">
                                    <div class="card">
                                        <div class="card-body">
                                        </div><!--end card-body-->
                                    </div><!--end card-->
                                </div><!--end col-->
                            </div><!--end row-->                                             
                        </div><!--end general detail-->
					</div><!--end tabs pages-->
				</div>
			</div>
		</div>
	</div>
</div>
</body>
`;
}else if(currentTab == 'services') {
	nBody+=`
						<div class="card-body">
							<div class="container1">
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('details')">Details</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('committees')">Committees</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('contact')">Contacts</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('exports')">Exports</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('items')">Products</label>
								<label style=" margin-right: 15px; padding: 5px;" onclick="changeCurrentTab('requests')">Requests</label>
								<label style=" margin-right: 15px; padding: 5px; color: #006738; border-bottom: 2px solid #006738;" onclick="changeCurrentTab('services')">E-service</label>
							</div>      
						</div><!--end card-body-->
					</div><!--end card-->
				</div><!--end col-->
			</div><!--end row and end of top part--> 
			<div class="row">
				<div class="col-12">
					<div class="tab-content detail-list" id="pills-tabContent">
						<div class="tab-pane fade show active" id="general">
                            <div class="row">
                            	<div class="col-12">
                                    <div class="card">
                                        <div class="card-body">
                                        </div><!--end card-body-->
                                    </div><!--end card-->
                                </div><!--end col-->
                            </div><!--end row-->                                             
                        </div><!--end general detail-->
					</div><!--end tabs pages-->
				</div>
			</div>
		</div>
	</div>
</div>
</body>
`;
}

	frappe.frappe_page.body = nBody;
    frappe.frappe_page.page.main.html(nBody);

	if(currentTab == 'exports') {
		new frappe.Chart("#dashboardChartEgp", {
			title: "EGP",
			data: {
				labels: ["الحالي" , "السابق"],
				datasets: [
					{
						name: 'الحالي',
						values: [currSeason.total_amount_in_egp.replace(/,/g, ''),0],
					},
					{
						name: 'السابق',
						values: [0,lastSeason.total_amount_in_egp.replace(/,/g, '')],
					},
				]
			},
			type: 'bar',
			colors: ['purple', 'black', 'green', 'blue'],
		});
		new frappe.Chart("#dashboardChartTon", {
			title: "Tons",
			data: {
				labels: ["الحالي" , "السابق"],
				datasets: [
					{
						name: 'الحالي',
						values: [currSeason.quantity_in_tons.replace(/,/g, ''),0],
					},
					{
						name: 'السابق',
						values: [0,lastSeason.quantity_in_tons.replace(/,/g, '')],
					},
				]
			},
			type: 'bar',
			colors: ['purple', 'black', 'green', 'blue'],
		});
		new frappe.Chart("#dashboardChartDollar", {
			title: "Dollar",
			data: {
				labels: ["الحالي" , "السابق"],
				datasets: [
					{
						name: 'الحالي',
						values: [currSeason.total_amount_in_usd.replace(/,/g, ''),0],
					},
					{
						name: 'السابق',
						values: [0,lastSeason.total_amount_in_usd.replace(/,/g, '')],
					},
				]
			},
			type: 'bar',
			colors: ['purple', 'black', 'green', 'blue'],
		});
		
	}
}
