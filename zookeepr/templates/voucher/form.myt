      <h2>Add a voucher code</h2>

      <div style="width: 600px; margin: auto;">

        <fieldset>

          <p class="label"><span class="mandatory">*</span><label for="voucher.count">Count:</label></p>
          <p class="entries"><% h.textfield('voucher.count', size=5) %></p>
          <p class="note">How many voucher codes to generate.</p>

          <p class="label"><span class="mandatory">*</span><label for="voucher.leader">Group leader:</label></p>
          <p class="entries"><% h.textfield('voucher.leader', size=5) %></p>
          <p class="note">ID of person who should be given the codes and allowed to see who's using them, as per the <% h.link_to('profile list', url=h.url(controller='person', action='index')) %>. If nobody, use your own ID: <% c.signed_in_person.id %></p>

          <p class="label"><label for="voucher.code">Code prefix:</label></p>
          <p class="entries"><% h.textfield('voucher.code', size=40) %></p>
          <p class="note">If you enter "foo", it might generate "foo-ooH4epe7". If blank, it'll just generate "ooH4epe7". Theoretically it might be a good idea to avoid 1, l, I, 0 and O, but I'm not sure how else one would spell IBM or GOOGLE :-)</p>

          <p class="label"><span class="mandatory">*</span>Product Selections</p>
          <p class="entries">
          <table>
% for category in c.product_categories:
%   if category.name in ['Ticket', 'Accomodation']:
            <tr>
              <td colspan="3" align="center"><h3><% category.name |h %></h3></td>
            </tr>
            <tr>
              <th>Product</th>
%       if category.name == 'Ticket':
              <th></th>
%       else:
              <th>Qty</th>
%       #endif
              <th>% Discount</th>
            </tr>
%       for product in category.products:
            <tr>
              <td><label for="products.product_<% product.id %>"><% product.description %></label></td>
%           if category.display == 'radio':
              <td><% h.radio_button('products.category_' + str(category.id), product.id) %>
# Add other display options here later, not adding select because we want accom to include a qty
%           else:
              <td><% h.textfield('products.product_' + str(product.id) + '_qty', size=3) %></td>
%           #endif
%           if category.display == 'radio' and category.products[0] == product:
              <td rowspan="<% len(category.products) %>"><% h.textfield('products.category_' + str(category.id) + '_percentage', size=3) %></td>
%           elif category.display == 'radio': pass
%           else:
              <td><% h.textfield('products.product_' + str(product.id) + '_percentage', size=3) %></td>
%           #endif
            </tr>
%       #endif
%   #endfor
% #endfor
          </table>
          </p>
          <p class="note">Discount percent is Between 0 and 100</p>


          <p class="label"><span class="mandatory">*</span><label for="voucher.comment">Comment:</label></p>
          <p class="entries"><% h.textfield('voucher.comment', size=60) %></p>
          <p class="note">Why are they getting a voucher? <b>This will appear on the invoices</b> as the item description for the negative amount - phrase accordingly...</p>
        </fieldset>
      </div>